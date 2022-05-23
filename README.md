# Tropical curve plotter
A python script to plot amazing tropical curves! :brazil:

![alt text](examples/elliptic.svg)

## Requirements

To install the dependencies for the project, run

  ```bash
    pip install -r requirements.txt
  ```

## Usage
To plot a curve simply run

  ```bash
    python plot.py input_file -o output_file 
  ```

where `input_file` is a file containing the list of triples `[x, y, coeff]`. For example the elliptic curve above is plotted by

  ```bash
    0 0 4
    1 0 1
    2 0 1
    3 0 4
    0 1 1
    1 1 0
    2 1 1
    0 2 1
    1 2 1
    0 3 4
  ```
## Additional arguments

  ```bash
    usage: plot.py [-h] [-c [{min,max}]] [-n] [-o OUTPUT] input

    positional arguments:
      input                 Input file name

    optional arguments:
      -h, --help            show this help message and exit
      -c [{min,max}], --convention [{min,max}]
                            Set the convention for the tropical semiring (default: min)
      -n, --newton          Plot the subdivided Newton polygon instead (default: False)
      -o OUTPUT, --output OUTPUT
                            Output file name (default = .png) (default: None)
  ```

## Examples

  ```bash
    python plot.py examples\funky.txt
  ```
![alt text](examples/funky.svg)

  ```bash
    python plot.py examples\funky.txt --newton
  ```
![alt text](examples/funky_newt.svg)

## About

I made this script as I needed to plot some complex curves and I found no other way to do that in a customizable way. Let me know if you find it useful or for features/bugs.

