1. ## Overview:
This file provides functionalities for assembling processed data into a final document. It handles sanitizing filenames, retrieving configuration, routing emergency configurations, and orchestrating the document assembly process using strategies. It also includes debugging utilities to inspect specific data structures.

2. ## Classes:
   - `AgentState`: Represents the state of an agent, potentially holding submission data, configuration, and metadata. (Assumed from import, not defined in provided snippet)

3. ## Functions & Methods:

| Name                     | Parameters                               | Responsibility                                                                                                                                                                                                                           |
| :----------------------- | :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sanitize_filename`      | `name: str`                              | Removes invalid characters from a given string and replaces spaces/hyphens with underscores to create a safe filename for the file system.                                                                                              |
| `assembly_node`          | `state: AgentState`                      | Orchestrates the assembly of a document. It retrieves submission data, determines submission type, rescues configuration if necessary, initializes a strategy, sanitizes firm and practice area names, creates a final filename, sets up temporary directories, converts markdown to richtext, calls the strategy to assemble the document in a temporary directory, moves the assembled document to its final destination, encodes the document to base64, and cleans up temporary files. Includes debugging prints for `publishable_matters`. |