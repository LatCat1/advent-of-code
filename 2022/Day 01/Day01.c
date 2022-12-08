#include <stdio.h>
#include <stdlib.h>

int maxPush(int new, int* array, int len){
    int t;
    for(int i = 0; i < len; i++){
        if(new > array[i]){
            t = array[i];
            array[i] = new;
            new = t;
        }
    }
}

int main(int* argc, char* argv[]){
    FILE* inputfile;
    int bufferLength = 255;
    char* buffer = malloc(bufferLength*sizeof(char));

    inputfile = fopen("Day01.txt", "r");
    int maxThree[] = {0,0,0};
    int current = 0;

    while(fgets(buffer, bufferLength, inputfile)){
        if(buffer[0] != '\n'){
            current += atoi(buffer);
        }else{
            maxPush(current, maxThree, 3);
            current = 0;
        }
    }
    maxPush(current, maxThree, 3);
    printf("Maximum: %d\nBest Three: %d\n", maxThree[0], maxThree[0] + maxThree[1] + maxThree[2]);

    fclose(inputfile);
    free(buffer);
}