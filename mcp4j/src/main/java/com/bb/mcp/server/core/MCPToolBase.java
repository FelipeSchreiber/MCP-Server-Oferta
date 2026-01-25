package com.bb.mcp.server.core;

import dev.langchain4j.agent.tool.ToolSpecification;

import java.util.List;

/**
 * Base interface for MCP tool services.
 * Mirrors the Python MCPToolBase abstract class.
 */
public interface MCPToolBase {
    
    /**
     * Get the domain this service belongs to.
     * 
     * @return The service domain
     */
    Domain getDomain();
    
    /**
     * Register tools with the MCP server.
     * Implementations should define their tools here.
     */
    void registerTools();
    
    /**
     * Get the number of tools provided by this service.
     * 
     * @return The tool count
     */
    int getToolCount();
    
    /**
     * Get tool specifications for this service.
     * 
     * @return List of tool specifications
     */
    List<ToolSpecification> getToolSpecifications();
    
    /**
     * Execute a tool by name with given parameters.
     * 
     * @param toolName The name of the tool to execute
     * @param parameters The parameters for the tool
     * @return The result of the tool execution
     */
    Object executeTool(String toolName, Object parameters);
}
