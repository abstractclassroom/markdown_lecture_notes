#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


// Initial Permutation Map
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

//Expansion Map
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

static const char shift_map[16] = {1,  1,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  1};

// S-Boxes
static const char Sbox[8][4][16] = {
    {
        // S-Box 0
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,  
         0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,  
         4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0, 
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    },{
        // S-Box 1
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,  
         3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,  
         0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15, 
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
    },{
        // S-Box 2
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,  
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,  
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
         1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
    },{
        // S-Box 3
         7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,  
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,  
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
         3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    },{
        // S-Box 4
         2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9, 
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6, 
         4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14, 
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    },{
        // S-Box 5
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
         9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
         4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    },{
        // S-Box 6
         4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
         1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
         6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    },{
        // S-Box 7
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
         1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
         7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
         2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    }
};

uint64_t des(uint64_t input, uint64_t key, char mode) {
    
    int i, j;
    char row, column;

    uint32_t C = 0;
    uint32_t D = 0;
    uint32_t left = 0;
    uint32_t right = 0;
    uint32_t s_output = 0;
    uint32_t f_function_res = 0;
    uint32_t temp = 0;
    uint64_t sub_key[16] = {0};
    uint64_t s_input = 0;
    uint64_t permuted_choice_1 = 0;
    uint64_t permuted_choice_2 = 0;
    uint64_t init_perm_res = 0;
    uint64_t inv_init_perm_res = 0;
    uint64_t pre_output = 0;
    
    // create permutation
    for (i = 0; i < 64; i++) {
        init_perm_res <<= 1;  //shift elements to left to add new LSB 
        init_perm_res |= (input >> (64-IP[i])) & 1; //add new LSB 
    }
    
    left = (uint32_t) ((init_perm_res & 0xffffffff00000000) >> 32);
    right = (uint32_t) init_perm_res & 0x00000000ffffffff;
    
    // key only has 56 bits after removing parity bits
    for (i = 0; i < 56; i++) {
        permuted_choice_1 <<= 1;
        permuted_choice_1 |= (key >> (64-PC1[i])) & 1;
    }
    C = (uint32_t) ((permuted_choice_1 >> 28) & 0x000000000fffffff);
    D = (uint32_t) (permuted_choice_1 & 0x000000000fffffff);
    
    for (i = 0; i< 16; i++) {
        for (j = 0; j < shift_map[i]; j++) {
            C = 0x0fffffff & (C << 1) | 1 & (C >> 27);
            D = 0x0fffffff & (D << 1) | 1 & (D >> 27);
        }
        permuted_choice_2 = 0;
        permuted_choice_2 = (((uint64_t) C) << 28) | (uint64_t) D ;
        sub_key[i] = 0;
        
        for (j = 0; j < 48; j++) {       
            sub_key[i] <<= 1;
            sub_key[i] |= (permuted_choice_2 >> (56-PC2[j])) & 1;
        }
    }

    for (i = 0; i < 16; i++) {
        s_input = 0;
        for (j = 0; j< 48; j++) {
            s_input <<= 1;
            s_input |= (uint64_t) ((right >> (32-E[j])) & 1);
        }
        s_input = (mode=='d') ? s_input ^ sub_key[15-i] : s_input ^ sub_key[i];
        for (j = 0; j < 8; j++) {
            // 0x0000840000000000 = 56 and 52 bit positions set to 1
            uint64_t mask = 0x0000840000000000;
            mask >>= 6*j;
            char row = (char) ((s_input & mask) >> (42-6*j));
            row = (row >> 4) | row & 0x01;
            // 0x0000780000000000 = 55, 54, 53, 52 bit positions set to 1
            mask = 0x0000780000000000;
            mask >>= 6*j;
            column = (char) ((s_input & (mask)) >> (43-6*j));
            s_output <<= 4;
            s_output |= (uint32_t) (Sbox[j][row][column] & 0x0f);
        }    
        f_function_res = 0;
        for (j = 0; j < 32; j++) {
            f_function_res <<= 1;
            f_function_res |= (s_output >> (32 - P[j])) & 1;
        }
        temp = right;
        right = left ^ f_function_res;
        left = temp;
    }
    pre_output = (((uint64_t) right) << 32) | (uint64_t) left;   
    for (i = 0; i < 64; i++) {
        inv_init_perm_res <<= 1;
        inv_init_perm_res |= (pre_output >> (64-FP[i])) & 1;
    }
    return inv_init_perm_res;
}

int main(int argc, const char * argv[]) {    
    uint64_t input = 0x01A1D6D039776742;
    uint64_t key = 0x7CA110454A1A6E57;
    uint64_t result = input;
    result = des(input, key, 'e');
    printf ("Ciphertext: %016llx\n", result);
    exit(0);
    
}