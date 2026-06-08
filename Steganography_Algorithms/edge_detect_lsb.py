import numpy as np
from PIL import Image
     
      def power_2(k):
          return 1 << k
      
      def k_bit_lsb(pixel, value, k):
          return pixel - (pixel % power_2(k)) + value
      
      def recover_k_bit_lsb(pixel, k):
         return pixel % power_2(k)
     
      class BitStream:
          def __init__(self, data=None, length=0):
              if data:
                  self.data = bytearray(data.encode('utf-8'))
                  self.length = len(self.data) * 8
              else:
                  self.data = bytearray(length)
                  self.length = length * 8
              self.pos = 0
     
          def get_bits(self, k):
              if self.pos + k > self.length:
                  k = self.length - self.pos
    
              if k == 0:
                  return 0
     
              byte_index = self.pos // 8
              bit_index = self.pos % 8
              bits = 0
     
              if bit_index + k <= 8:
                  bits = (self.data[byte_index] >> bit_index) & ((1 << k) - 1)
              else:
                  bits_from_byte1 = 8 - bit_index
                  bits = (self.data[byte_index] >> bit_index) & ((1 << bits_from_byte1) - 1)
    
                  if byte_index + 1 < len(self.data):
                      bits_from_byte2 = k - bits_from_byte1
                      bits |= (self.data[byte_index + 1] & ((1 << bits_from_byte2) - 1)) << bits_from_byte1
     
              self.pos += k
              return bits
      
          def write_bits(self, bits, k):
              if self.pos + k > self.length:
                  k = self.length - self.pos
    
              if k == 0:
                  return
     
              byte_index = self.pos // 8
              bit_index = self.pos % 8
     
              if bit_index + k <= 8:
                  mask = ((1 << k) - 1) << bit_index
                  self.data[byte_index] = (self.data[byte_index] & ~mask) | ((bits << bit_index) & mask)
              else:
                  bits_to_byte1 = 8 - bit_index
                  mask1 = ((1 << bits_to_byte1) - 1) << bit_index
                  self.data[byte_index] = (self.data[byte_index] & ~mask1) | ((bits << bit_index) & mask1)
      
                  if byte_index + 1 < len(self.data):
                     bits_to_byte2 = k - bits_to_byte1
                     mask2 = (1 << bits_to_byte2) - 1
                     self.data[byte_index + 1] = (self.data[byte_index + 1] & ~mask2) | (bits >> bits_to_byte1)
     
              self.pos += k
     
          def has_next(self):
              return self.pos < self.length
     
          def get_data(self):
              return self.data.decode('utf-8', errors='ignore')
     
      def edge_detect_encrypt(img_path, msg, block_size, non_edge_bits, edge_bits):
          img = Image.open(img_path).convert('L')
          st_img = np.array(img)
          edge = np.array(img.filter(ImageFilter.FIND_EDGES))
          stream = BitStream(data=msg)
     
          size = edge.size - (edge.size % block_size)
          block_id = 0
     
          for i in range(0, size, block_size):
              if not stream.has_next():
                  break
    
              for j in range(1, block_size):
                  if not stream.has_next():
                      break
     
                  pixel_index = i + j
                  if pixel_index < st_img.size:
                      if edge.flat[pixel_index] == 255:
                          block_id += 2**(j - 1)
                          bits = stream.get_bits(edge_bits)
                          st_img.flat[pixel_index] = k_bit_lsb(st_img.flat[pixel_index], bits, edge_bits)
                      else:
                          bits = stream.get_bits(non_edge_bits)
                          st_img.flat[pixel_index] = k_bit_lsb(st_img.flat[pixel_index], bits, non_edge_bits)
    
               if i < st_img.size:
                st_img.flat[i] = k_bit_lsb(st_img.flat[i], block_id, block_size - 1)
                block_id = 0
   
          return Image.fromarray(st_img)
    
      def edge_detect_decrypt(img_path, msg_len, block_size, non_edge_bits, edge_bits):
          img = Image.open(img_path).convert('L')
          st_img = np.array(img)
          stream = BitStream(length=msg_len)
    
          size = st_img.size - st_img.size % block_size
    
          for i in range(0, size, block_size):
              if not stream.has_next():
                  break
    
              if i < st_img.size:
                  block_id = recover_k_bit_lsb(st_img.flat[i], block_size - 1)
    
                  for j in range(1, block_size):
                      if not stream.has_next():
                          break
      
                      pixel_index = i + j
                      if pixel_index < st_img.size:
                          if (block_id & 1) == 1:
                              bits = recover_k_bit_lsb(st_img.flat[pixel_index], edge_bits)
                              stream.write_bits(bits, edge_bits)
                          else:
                              bits = recover_k_bit_lsb(st_img.flat[pixel_index], non_edge_bits)
                              stream.write_bits(bits, non_edge_bits)
                      block_id >>= 1
    
          return stream.get_data()
