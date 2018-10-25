/* Copyright (c) 2017 Mozilla */
/*
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:

   - Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

   - Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/


//old
//rec -c 1 -b 16 -d | ./rnn_test melm.wav mlemm.wav
//arecord -v -f dat -t raw | ./rnn_test out.pcm ; sox -t raw -r 48000 -b 16 -c 2 -L -e signed-integer out.pcm out.wav gain -n -3
//arecord -v -f dat -t raw | ./rnn_test out.pcm ; sox -t raw -r 48000 -b 16 -c 2 -L -e signed-integer out.pcm out.wav vol 3 db


//NEW
// gcc remove_noise.c -lrnnoise -o remove_noise
//arecord -v -f S16_LE -c1 -r48000 -t raw | ./remove_noise out.pcm ; sox -t raw -r 48000 -b 16 -c 1 -L -e signed-integer out.pcm out.wav vol 3 db

// arecord -v -f S16_LE -c1 -r48000 -t raw | sox -c 1 -r 48000 -b 16 -L -e signed-integer -t raw - -c 1 -r 48000 -b 16 -L -e signed-integer -t raw - vol 15 dB | ./remove_noise /dev/stdout | sox -t raw -r 48000 -b 16 -c 1 -L -e signed-integer - -r 16k out_16.wav
// /usr/local/bin/pocketsphinx_continuous -logfn /dev/null -infile '/home/shoaib/Desktop/rnnoise/examples/out_16.wav' > out.txt; cat out.txt


#include <stdio.h>
#include "rnnoise.h"

#define FRAME_SIZE 480

int main(int argc, char **argv) {
  int i;
  int first = 1;
  float x[FRAME_SIZE];
  FILE *fout;
  DenoiseState *st;
  st = rnnoise_create();
  if (argc!=2) {
    fprintf(stderr, "audio | usage: %s <output denoised>\n", argv[0]);
    return 1;
  }
  fout = fopen(argv[1], "w");
  while (1) {
    short tmp[FRAME_SIZE];
    fread(tmp, sizeof(short), FRAME_SIZE, stdin);
    if (feof(stdin)) break;
    for (i=0;i<FRAME_SIZE;i++) x[i] = tmp[i];
    rnnoise_process_frame(st, x, x);
    for (i=0;i<FRAME_SIZE;i++) tmp[i] = x[i];
    if (!first) fwrite(tmp, sizeof(short), FRAME_SIZE, fout);
    first = 0;
  }
  rnnoise_destroy(st);
  fclose(stdin);
  fclose(fout);
  return 0;
}

