#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


// Initial Permutation Map
// Permutation Map 64 bits -> 64 bits
static const char IP[64] = {
    58, 50, 42, 34, 26, 18, 10,  2, 
    60, 52, 44, 36, 28, 20, 12,  4, 
    62, 54, 46, 38, 30, 22, 14,  6, 
    64, 56, 48, 40, 32, 24, 16,  8, 
    57, 49, 41, 33, 25, 17,  9,  1, 
    59, 51, 43, 35, 27, 19, 11,  3, 
    61, 53, 45, 37, 29, 21, 13,  5, 
    63, 55, 47, 39, 31, 23, 15,  7
};

// Final Permutation Map 
// Permutation Map 64 bits -> 64 bits
static const char FP[64] = {
    40,  8, 48, 16, 56, 24, 64, 32, 
    39,  7, 47, 15, 55, 23, 63, 31, 
    38,  6, 46, 14, 54, 22, 62, 30, 
    37,  5, 45, 13, 53, 21, 61, 29, 
    36,  4, 44, 12, 52, 20, 60, 28, 
    35,  3, 43, 11, 51, 19, 59, 27, 
    34,  2, 42, 10, 50, 18, 58, 26, 
    33,  1, 41,  9, 49, 17, 57, 25
};

//Expansion Map 32 bits -> 48 bits
static const char E[] = {
    32,  1,  2,  3,  4,  5,  
     4,  5,  6,  7,  8,  9,  
     8,  9, 10, 11, 12, 13, 
    12, 13, 14, 15, 16, 17, 
    16, 17, 18, 19, 20, 21, 
    20, 21, 22, 23, 24, 25, 
    24, 25, 26, 27, 28, 29, 
    28, 29, 30, 31, 32,  1
};

//Permutation Map 32 bits -> 32 bits
static const char P[] = {
    16,  7, 20, 21, 
    29, 12, 28, 17, 
     1, 15, 23, 26, 
     5, 18, 31, 10, 
     2,  8, 24, 14, 
    32, 27,  3,  9, 
    19, 13, 30,  6, 
    22, 11,  4, 25
};

//Perm 1 Key & Remove Parity Bits
// Permutation Map 64 bits -> 56 bits
static const char PC1[] = {
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
};

//Perm 2 Key
// Permutation Map 56 bits -> 48 bits
static const char PC2[] = {
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
};

//Shifts for each round
static const char shift_map[16] = {1,  1,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  1};

// S-Boxes
static const char Sbox[8][4][16] = {
    {// S-Box 0
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,  
         0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,  
         4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0, 
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    },{// S-Box 1
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,  
         3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,  
         0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15, 
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
    },{// S-Box 2
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,  
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,  
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
         1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
    },{// S-Box 3
         7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,  
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,  
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
         3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    },{// S-Box 4
         2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9, 
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6, 
         4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14, 
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    },{// S-Box 5
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
         9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
         4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    },{// S-Box 6
         4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
         1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
         6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    },{// S-Box 7
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
         1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
         7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
         2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    }
};


//applies permutation map
static inline uint64_t apply_map(uint64_t initial_bit_block, const char *map, int initial_size, int result_size) {
    uint64_t result = 0;
    for (int i = 0; i < result_size; i++) {
        result <<= 1;
        result |= (initial_bit_block >> (initial_size-map[i])) & 1;
    }
    return result;
}

//splits block (64 bits or less) into two equal parts
static inline void split_bit_block(uint64_t bit_block, uint32_t *left, uint32_t *right, int length) {
    uint64_t bit_mask_left = ((uint64_t)1 << ((length + 1) / 2)) - 1;
    uint64_t bit_mask_right = ((uint64_t)1 << (length / 2)) - 1;
    *right = (uint32_t) (bit_block & bit_mask_right);
    *left = (uint32_t) ((bit_block >> (length / 2)) & bit_mask_left);
}

//applies rotations to left and right side of key
static inline void apply_rotations_lr_28_key(uint32_t *left, uint32_t *right, int i) {
    for (int j = 0; j < shift_map[i]; j++) {
        *left = 0x0fffffff & (*left << 1) | 1 & (*left >> 27);
        *right = 0x0fffffff & (*right << 1) | 1 & (*right >> 27);
    }
}

//creates 16 subkeys having 48 bits created from original 56 bit key
static inline void create_16_sub_keys(uint64_t perm_1_key_56, uint64_t *sub_key) {
    uint32_t left_28;
    uint32_t right_28;
    split_bit_block(perm_1_key_56, &left_28, &right_28, 56);
    for (int i = 0; i< 16; i++) {
        apply_rotations_lr_28_key(&left_28, &right_28, i);
        u_int64_t combined_left_right = (((uint64_t) left_28) << 28) | (uint64_t) right_28 ;
        sub_key[i] = apply_map(combined_left_right, PC2, 56, 48);
    }
}

//applies 16 fiestel rounds
static inline uint_fast64_t apply_16_fiestel_rounds(uint32_t right_32, uint32_t left_32, uint64_t *sub_key, char mode) {
    uint32_t s_box_output = 0;
    uint64_t bit_mask;
    for (int i = 0; i < 16; i++) {
        uint64_t expanded_rhs = apply_map(right_32, E, 32, 48);
        expanded_rhs ^= (mode=='d') ? sub_key[15-i] : sub_key[i];
        for (int j = 0; j < 8; j++) {
            bit_mask = 0x0000840000000000 >> 6*j; //56 and 52 bit positions set to 1 shifted 6*j bits to the right
            char row = (char) ((expanded_rhs & bit_mask) >> (42-6*j));
            row = (row >> 4) | row & 0x01;
            bit_mask = 0x0000780000000000 >> 6*j; //55, 54, 53, 52 bit positions set to 1 shifted 6*j bits to the right
            char column = (char) ((expanded_rhs & (bit_mask)) >> (43-6*j));
            s_box_output <<= 4;
            s_box_output |= (uint32_t) (Sbox[j][row][column] & 0x0f);
        } 
        uint32_t fiestel_output = apply_map(s_box_output, P, 32, 32);
        uint32_t tmp = right_32;
        right_32 = left_32 ^ fiestel_output;
        left_32 = tmp;
    }
    return (((uint64_t) right_32) << 32) | (uint64_t) left_32;   
}


uint64_t des(uint64_t initial_bit_block, uint64_t key, char mode) {
    uint64_t permutated_msg_block = apply_map(initial_bit_block, IP, 64, 64);
    uint32_t perm_msg_block_left_32, perm_msg_block_right_32;
    split_bit_block(permutated_msg_block, &perm_msg_block_left_32, &perm_msg_block_right_32, 64);
    uint64_t perm_1_key_56 = apply_map(key, PC1, 64, 56);
    uint32_t left_28, right_28;
    split_bit_block(perm_1_key_56, &left_28, &right_28, 56);
    uint64_t sub_key[16];
    create_16_sub_keys(perm_1_key_56, sub_key);
    u_int64_t fiestel_rounds_output = apply_16_fiestel_rounds(perm_msg_block_right_32, perm_msg_block_left_32, sub_key, mode);
    uint64_t FP_output = apply_map(fiestel_rounds_output, FP, 64, 64);
    return FP_output;
}

int main(int argc, const char * argv[]) {    
    uint64_t initial_bit_block = 0x01A1D6D039776742;
    uint64_t key = 0x7CA110454A1A6E57;
    uint64_t result = initial_bit_block;
    result = des(initial_bit_block, key, 'e');
    printf ("Ciphertext: %016llx\n", result);
    result = des(result, key, 'd');
    printf ("Plaintext: %016llx\n", result);
    exit(0);
    
}