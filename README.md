# How it works

#### This programm makes a set of images that describes graph state in each algorithm step

## Example of generated graph state:

<p align="center">
 <img width="400px" src="img/graph15.png" alt="qr"/>
</p>

### Label in the top is the name of the file



### node colors:
- ![#FF0000](https://placehold.co/15x15/ff0000/ff0000.png) red    - passed
- ![#00FF00](https://placehold.co/15x15/00ff00/00ff00.png) green  - current
- ![#ffffff](https://placehold.co/15x15/ffff00/ffff00.png) yellow - neighbours of passed and current nodes

### edges colors:
- ![#FF0000](https://placehold.co/15x15/ff0000/ff0000.png) red   - passed
- ![#000000](https://placehold.co/15x15/000000/000000.png) black - other
### red edges define the optimal route tree

### Edge number: 
- weight
### Node numbers (from top to bottom):
- node number
- node weight (maximum edge's weight for edges in optimal root). default: 1000000
- previous node. default: -1
#### default means there isn't any optimal roots at this moment




# How to use it

#### Make your own graph like in example in `main.py`
#### To start  
