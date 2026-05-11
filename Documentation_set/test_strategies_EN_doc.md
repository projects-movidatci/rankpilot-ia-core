# Overview:
This file contains unit tests for the `Legal500Strategy` and `ChambersStrategy` classes. It verifies their initialization, configuration loading, and basic auditing functionality.

# Classes:
- `TestStrategies`: A test class inheriting from `unittest.TestCase` to group strategy-related tests.

# Functions & Methods:
| Name | Parameters | Responsibility |
|---|---|---|
| `test_legal500_strategy_init` | `self` | Tests the initialization of `Legal500Strategy`, checks for the presence of `config`, verifies the 'name' attribute in the config, and confirms that the `audit` method returns a non-empty list of gaps. |
| `test_chambers_strategy_init` | `self` | Tests the initialization of `ChambersStrategy`, checks for the presence of `config`, verifies the 'name' attribute in the config, and confirms that the `audit` method returns a non-empty list of gaps. |