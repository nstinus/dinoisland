#include "Dinosaur.h"

int main(int argc, char* argv[])
{
  DinosaurIf d = DinosaurIf();
  RegisterClientResult r;
  d.registerClient(r, "xzoiid@gmail.com", "xzoiid", 1);
  return 0;
}
