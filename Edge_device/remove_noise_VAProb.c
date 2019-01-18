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
    short tmp[FRAME_SIZE+1+3];
    //End Sequence
    tmp[FRAME_SIZE+1] = 0;
    tmp[FRAME_SIZE+2] = 126;
    tmp[FRAME_SIZE+3] = 0;
    //End Sequence*
    fread(tmp, sizeof(short), FRAME_SIZE, stdin);
    if (feof(stdin)) break;
    for (i=0;i<FRAME_SIZE;i++) x[i] = tmp[i];
    tmp[FRAME_SIZE] = (short)(rnnoise_process_frame(st, x, x)*100.0);
    for (i=0;i<FRAME_SIZE;i++) tmp[i] = x[i];
    if (!first){
    	fwrite(tmp, sizeof(short), FRAME_SIZE+1+3, fout);// data-prob-endseq
    }
    first = 0;
  }
  rnnoise_destroy(st);
  fclose(stdin);
  fclose(fout);
  return 0;
}