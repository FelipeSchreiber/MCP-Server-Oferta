package com.bb.mcp.server.controller;

import com.bb.mcp.server.core.Domain;
import com.bb.mcp.server.core.MCPToolBase;
import com.bb.mcp.server.core.MCPToolFactory;
import dev.langchain4j.agent.tool.ToolSpecification;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import lombok.extern.slf4j.Slf4j;

import java.util.*;
import java.util.stream.Collectors;

/**
 * REST controller for MCP tool execution.
 * Provides HTTP endpoints for tool discovery and execution.
 */
@Slf4j
@Path("/api/mcp")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class MCPController {
    
    @Inject
    MCPToolFactory factory;
    
    /**
     * Get server information and available tools.
     * 
     * @return Server info
     */
    @GET
    @Path("/info")
    public Response getServerInfo() {
        MCPToolFactory.ToolSummary summary = factory.getToolSummary();
        
        Map<String, Object> info = new HashMap<>();
        info.put("server_name", "BB MCP4J Server");
        info.put("total_services", summary.getTotalServices());
        info.put("total_tools", summary.getTotalTools());
        info.put("services", summary.getServices());
        
        return Response.ok(info).build();
    }
    
    /**
     * List all available tools.
     * 
     * @return List of tool specifications
     */
    @GET
    @Path("/tools")
    public Response listTools() {
        Map<String, Object> response = new HashMap<>();
        List<Map<String, Object>> tools = new ArrayList<>();
        
        for (MCPToolBase service : factory.getAllServices().values()) {
            for (ToolSpecification spec : service.getToolSpecifications()) {
                Map<String, Object> toolInfo = new HashMap<>();
                toolInfo.put("name", spec.name());
                toolInfo.put("description", spec.description());
                toolInfo.put("domain", service.getDomain().getValue());
                tools.add(toolInfo);
            }
        }
        
        response.put("tools", tools);
        response.put("count", tools.size());
        
        return Response.ok(response).build();
    }
    
    /**
     * Get tools for a specific domain.
     * 
     * @param domainName The domain name
     * @return List of tools in that domain
     */
    @GET
    @Path("/tools/{domain}")
    public Response getToolsByDomain(@PathParam("domain") String domainName) {
        try {
            Domain domain = Domain.valueOf(domainName.toUpperCase());
            MCPToolBase service = factory.getService(domain);
            
            if (service == null) {
                return Response.status(Response.Status.NOT_FOUND).build();
            }
            
            Map<String, Object> response = new HashMap<>();
            response.put("domain", domain.getValue());
            response.put("tool_count", service.getToolCount());
            response.put("tools", service.getToolSpecifications());
            
            return Response.ok(response).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).build();
        }
    }
    
    /**
     * Execute a tool.
     * 
     * @param toolName The name of the tool to execute
     * @param parameters The tool parameters
     * @return Tool execution result
     */
    @POST
    @Path("/tools/{toolName}/execute")
    public Response executeTool(
            @PathParam("toolName") String toolName,
            Map<String, Object> parameters) {
        
        log.info("Executing tool: {} with parameters: {}", toolName, parameters);
        
        try {
            // Find the service that has this tool
            MCPToolBase targetService = null;
            for (MCPToolBase service : factory.getAllServices().values()) {
                List<String> toolNames = service.getToolSpecifications().stream()
                        .map(ToolSpecification::name)
                        .collect(Collectors.toList());
                if (toolNames.contains(toolName)) {
                    targetService = service;
                    break;
                }
            }
            
            if (targetService == null) {
                Map<String, Object> error = new HashMap<>();
                error.put("error", "Tool not found: " + toolName);
                return Response.status(Response.Status.NOT_FOUND).entity(error).build();
            }
            
            // Execute the tool
            Object result = targetService.executeTool(toolName, parameters);
            
            Map<String, Object> response = new HashMap<>();
            response.put("tool", toolName);
            response.put("result", result);
            response.put("status", "success");
            
            return Response.ok(response).build();
            
        } catch (Exception e) {
            log.error("Error executing tool: {}", toolName, e);
            
            Map<String, Object> error = new HashMap<>();
            error.put("error", e.getMessage());
            error.put("tool", toolName);
            error.put("status", "error");
            
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity(error).build();
        }
    }
    
    /**
     * Health check endpoint.
     * 
     * @return Health status
     */
    @GET
    @Path("/health")
    public Response health() {
        Map<String, String> health = new HashMap<>();
        health.put("status", "healthy");
        health.put("server", "BB MCP4J Server");
        return Response.ok(health).build();
    }
}

