#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char string_byte(const void* buf, int i) {
	return (((const unsigned char*) buf)[i] ^ i) + 0x23;
}

void string_byte_r(void* buf, int start, int size) {
	unsigned char* _buf = buf;
	for (int i = start; i < start + size; i++) {
		_buf[i] = (_buf[i] - 0x23) ^ i;
	}
}

unsigned int to_uint(const void* s, int at) {
	unsigned int v = 0;
	for (int i = 0; i < 4; i++) {
		v |= string_byte(s, i + at) << (8 * i);
	}
	return v;
}

void RC4Init(unsigned char* rc4box, const char* key, unsigned int keylen) {
	char k[256];
	for (int i = 0; i < 256; i++) {
		rc4box[i] = i;
		k[i] = string_byte(key, i % keylen);
	}
	for (int i = 0, j = 0; i < 256; i++) {
		j = (j + rc4box[i] + k[i]) & 0xff;
		int tmp = rc4box[i];
		rc4box[i] = rc4box[j];
		rc4box[j] = tmp;
	}
}

void RC4Encrypt(unsigned char* rc4box, char* src, unsigned int len) {
	for (int i = 0, j = 0, k = 0; k < len; k++) {
		i = (i + 1) & 0xff;
		j = (j + rc4box[i]) & 0xff;
		int tmp = rc4box[i];
		rc4box[i] = rc4box[j];
		rc4box[j] = tmp;
		tmp = string_byte(src, k) ^ rc4box[(rc4box[i] - rc4box[j]) & 0xff];
		src[k] = tmp;
		j = (j + tmp) & 0xff;
	}
}

void RC4Decrypt(unsigned char* rc4box, char* src, unsigned int len) {
	for (int i = 0, j = 0, k = 0; k < len; k++) {
		i = (i + 1) & 0xff;
		j = (j + rc4box[i]) & 0xff;
		int tmp = rc4box[i];
		rc4box[i] = rc4box[j];
		rc4box[j] = tmp;
		tmp = src[k];
		src[k] ^= rc4box[(rc4box[i] - rc4box[j]) & 0xff];
		j = (j + tmp) & 0xff;
	}
	string_byte_r(src, 0, len);
}

void rc4_do_encrypt(void* buf, size_t buf_len, const void* key, size_t keylen) {
	unsigned char rc4box[256];
	RC4Init(rc4box, (const char*) key, keylen);
	RC4Encrypt(rc4box, (char*) buf, buf_len);
}

void rc4_do_decrypt(void* buf, size_t buf_len, const void* key, size_t keylen) {
	unsigned char rc4box[256];
	RC4Init(rc4box, (const char*) key, keylen);
	RC4Decrypt(rc4box, (char*) buf, buf_len);
}

void tea_encrypt(unsigned int* v0, unsigned int* v1, const void* k) {
	unsigned int sum = 0;
	unsigned int delta = 0x12345678;
	unsigned int k0 = to_uint(k, 0), k1 = to_uint(k, 4), k2 = to_uint(k, 8), k3 = to_uint(k, 12);
	for (int i = 0; i < 32; i++) {
		rc4_do_encrypt(&delta, 4, k, 16);
		delta = to_uint(&delta, 0);
		sum += delta;
		*v0 += ((*v1 << 4) + k0) ^ (*v1 + sum) ^ ((*v1 >> 5) + k1);
		*v1 += ((*v0 << 4) + k2) ^ (*v0 + sum) ^ ((*v0 >> 5) + k3);
	}
}

void tea_decrypt(unsigned int* v0, unsigned int* v1, const void* k) {
	unsigned int sum = 0;
	unsigned int delta = 0x12345678;
	unsigned int k0 = to_uint(k, 0), k1 = to_uint(k, 4), k2 = to_uint(k, 8), k3 = to_uint(k, 12);
	for (int i = 0; i < 32; i++) {
		rc4_do_encrypt(&delta, 4, k, 16);
		delta = to_uint(&delta, 0);
		sum += delta;
	}
	for (int i = 0; i < 32; i++) {
		*v1 -= ((*v0 << 4) + k2) ^ (*v0 + sum) ^ ((*v0 >> 5) + k3);
		*v0 -= ((*v1 << 4) + k0) ^ (*v1 + sum) ^ ((*v1 >> 5) + k1);
		sum -= delta;
		string_byte_r(&delta, 0, 4);
		rc4_do_decrypt(&delta, 4, k, 16);
	}
}

int main() {
	const char* key = "thisshouldbeakey";
	/*
	char flag[] = "0123456789abcdef0123456789abcdef";
	puts(flag);
	rc4_do_encrypt(flag, 32, key, 16);
	for (int i = 0; i < 4; i++) {
		unsigned int v0 = to_uint(flag, 8 * i);
		unsigned int v1 = to_uint(flag, 8 * i + 4);
		tea_encrypt(&v0, &v1, key);
		*(unsigned int*) (flag + 8 * i) = v0;
		*(unsigned int*) (flag + 8 * i + 4) = v1;
	}
	for (int i = 0; i < 32; i++) {
		printf("%02x", string_byte(flag, i));
	}
	putchar('\n');
	*/
	char flag[] = "\xac\x0c\x00\x27\xf0\xe4\x03\x2a\xcf\x7b\xd2\xc3\x7b\x25\x2a\x93\x30\x91\xa0\x6a\xee\xbc\x07\x2c\x98\x0f\xa6\x2c\x24\xf4\x86\xc6";
	string_byte_r(flag, 0, 32);

	for (int i = 0; i < 4; i++) {
		tea_decrypt((unsigned int*) (flag + 8 * i), (unsigned int*) (flag + 8 * i + 4), key);
	}
	string_byte_r(flag, 0, 32);
	rc4_do_decrypt(flag, 32, key, 16);
	printf("SUCTF{%s}\n", flag);
	return 0;
}

// SUCTF{341528c2bde511efade200155d8503ef}