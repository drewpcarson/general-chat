from typing import Dict, List, Any

class SchemaConverter:
    @staticmethod
    def to_anthropic(openai_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI tool format to Anthropic format"""
        anthropic_tools = []
        
        for tool in openai_tools:
            if tool["type"] != "function":
                continue
                
            function = tool["function"]
            anthropic_tool = {
                "name": function["name"],
                "description": function["description"],
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": function.get("required", [])
                }
            }
            
            # Convert properties
            for prop_name, prop_details in function["parameters"]["properties"].items():
                anthropic_tool["input_schema"]["properties"][prop_name] = {
                    "type": prop_details["type"],
                    "description": prop_details.get("description", "")
                }
                
                # Handle enums
                if "enum" in prop_details:
                    anthropic_tool["input_schema"]["properties"][prop_name]["enum"] = prop_details["enum"]
                
                # Handle not/enum for exclusions
                if "not" in prop_details and "enum" in prop_details["not"]:
                    anthropic_tool["input_schema"]["properties"][prop_name]["not"] = {
                        "enum": prop_details["not"]["enum"]
                    }
            
            anthropic_tools.append(anthropic_tool)
            
        return anthropic_tools

    @staticmethod
    def to_openai(anthropic_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert Anthropic tool format to OpenAI format"""
        openai_tools = []
        
        for tool in anthropic_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": tool["input_schema"].get("required", [])
                    }
                }
            }
            
            # Convert properties
            for prop_name, prop_details in tool["input_schema"]["properties"].items():
                openai_tool["function"]["parameters"]["properties"][prop_name] = {
                    "type": prop_details["type"],
                    "description": prop_details.get("description", "")
                }
                
                # Handle enums
                if "enum" in prop_details:
                    openai_tool["function"]["parameters"]["properties"][prop_name]["enum"] = prop_details["enum"]
                
                # Handle not/enum for exclusions
                if "not" in prop_details and "enum" in prop_details["not"]:
                    openai_tool["function"]["parameters"]["properties"][prop_name]["not"] = {
                        "enum": prop_details["not"]["enum"]
                    }
            
            openai_tools.append(openai_tool)
            
        return openai_tools