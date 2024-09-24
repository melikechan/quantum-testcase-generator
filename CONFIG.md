# Input Configuration

For every problem, you have to create a _format_ file that will be used to run your code.

This file **must be a JSON** file, and you can find an example of the _format_ file [here](sample_format.json).

## Structure of the _format_ file

Format file is an array of objects, where each object represents a _single line_ of the input.

### Fields of the object

- `lineNumber` (int, required): The line number of the input.
- `inputType` (string, required): The type of the input. It can be one of the following:
  - `single`: A single value.
  - `tuple`: A tuple of values.
  - `array`: An array of values. (1-D or 2-D)
  - `graph`: A graph with multiple nodes and edges.
- `args` (object, required): Arguments for the `inputType`. It has values based on the `inputType`:
  - `single` (for numeric values):
    - `valueLowerBound` (int, required): The lower bound of the value.
    - `valueUpperBound` (int, required): The upper bound of the value.
  - `single` (for string values):
    - `length` (int, optional): The length of the value. (Default: 1)
    - `chars` (string, optional): The characters that can be used in the value. It can take at least one of the following values:
      - `lower`: Lowercase alphabetic characters (a-z)
      - `upper`: Uppercase alphabetic characters (A-Z)
      - `numeric`: Numbers (0-9)
      - `special`: Special characters (`!@#$%^&*()_+`)
      - `custom`: Custom characters, if used, then `customChars` is required.
        - `customChars` (list, required): The custom characters that can be used in the value.
  - `tuple`:
    - `valueCount` (int, required): The number of values in the tuple.
    - `valueType` (list, required): The type of the values in the tuple. It can be a `single`.
  - `array`:
    - `dimensionCount` (int, required): The number of dimensions in the array. (1 or 2)
    - `valueCount` (int, required): The number of values in the array.
    - `valueType` (string, required): The type of the values in the array. It can be a `single` or `tuple`.
    - `valueArgs` (object, optional): Arguments for the `valueType`.
  - `graph`:
    - `nodeLowerBound` (int, required): The lower bound of the number of nodes.
    - `nodeUpperBound` (int, required): The upper bound of the number of nodes.
    - `edgeLowerBound` (int, required): The lower bound of the number of edges.
    - `edgeUpperBound` (int, required): The upper bound of the number of edges.
    - `weightLowerBound` (int, optional): The lower bound of the weight of the edges. (Default: 1)
    - `weightUpperBound` (int, optional): The upper bound of the weight of the edges. (Default: 100)
    - `isDirected` (boolean, required): Whether the graph is directed or not.
    - `isWeighted` (boolean, required): Whether the graph is weighted or not.
    - `constraints` (list, optional): The constraints for the graph. It can take at least one of the following values:
      - `tree`: The graph is a tree.
      - `acyclic`: The graph is acyclic.
      - `bipartite`: The graph is bipartite.
      - `multi`: The graph can have multiple edges between two nodes. (can not be used with `tree` or `acyclic` constraints)
      - `self`: The graph can have self loops. (can not be used with `tree` or `acyclic` constraints)
