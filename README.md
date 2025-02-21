# BloodrayneReversing
Working on reversing Bloodrayne's archive and model formats.

Inspired by daeken's "Becoming a Full Stack Reverse Engineer" (https://www.youtube.com/watch?v=9vKG8-TnawY):
- Pick a 3d game, preferably late 90s to mid 00s, running on a custom engine
  - This is important because off-the-shelf engines typically have more-open formats and we don’t want that
- Reverse-engineer its data archive format
  - Write an unpacker
- Reverse-engineer its model format
  - Write a renderer
    - Bonus points: write it for OpenGL or WebGL and then port to Vulkan
      Understanding 3d APIs is crazy valuable later
