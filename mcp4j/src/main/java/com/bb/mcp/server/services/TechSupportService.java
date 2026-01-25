package com.bb.mcp.server.services;

import com.bb.mcp.server.core.Domain;
import com.bb.mcp.server.core.MCPToolBase;
import com.bb.mcp.server.utils.ResponseFormatter;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.agent.tool.ToolSpecification;
import jakarta.enterprise.context.ApplicationScoped;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Technical Support service with IT/helpdesk tools.
 * Mirrors the Python TechSupportService class.
 */
@Slf4j
@ApplicationScoped
public class TechSupportService implements MCPToolBase {
    
    private final Domain domain = Domain.TECH_SUPPORT;
    private final int toolCount = 2; // reset_password, check_system_status
    private final Map<String, java.util.function.Function<Object, Object>> tools = new HashMap<>();
    
    public TechSupportService() {
        registerTools();
    }
    
    @Override
    public Domain getDomain() {
        return domain;
    }
    
    @Override
    public int getToolCount() {
        return toolCount;
    }
    
    @Override
    public void registerTools() {
        tools.put("reset_password", params -> {
            Map<String, Object> paramMap = (Map<String, Object>) params;
            String username = (String) paramMap.get("username");
            return resetPassword(username);
        });
        
        tools.put("check_system_status", params -> {
            Map<String, Object> paramMap = (Map<String, Object>) params;
            String systemName = (String) paramMap.get("system_name");
            return checkSystemStatus(systemName);
        });
        
        log.info("Registered {} tools for {} domain", toolCount, domain);
    }
    
    @Override
    public List<ToolSpecification> getToolSpecifications() {
        List<ToolSpecification> specs = new ArrayList<>();
        
        specs.add(ToolSpecification.builder()
                .name("reset_password")
                .description("Reset password for a user account. Parameters: username (string)")
                .build());
        
        specs.add(ToolSpecification.builder()
                .name("check_system_status")
                .description("Check the operational status of a system. Parameters: system_name (string)")
                .build());
        
        return specs;
    }
    
    @Override
    public Object executeTool(String toolName, Object parameters) {
        java.util.function.Function<Object, Object> tool = tools.get(toolName);
        if (tool == null) {
            throw new IllegalArgumentException("Unknown tool: " + toolName);
        }
        return tool.apply(parameters);
    }
    
    /**
     * Tool: Reset user password.
     * 
     * @param username The username to reset
     * @return Formatted response
     */
    @Tool("Reset password for a user account")
    public String resetPassword(String username) {
        log.info("Resetting password for username: {}", username);
        
        Map<String, Object> content = new HashMap<>();
        content.put("username", username);
        content.put("status", "success");
        content.put("temporary_password", "TempPass123!");
        content.put("expires_in", "24 hours");
        
        return ResponseFormatter.formatMcpResponse(
                "Password Reset Result",
                content,
                String.format("Successfully reset password for user '%s'", username),
                "Please inform the user to change their temporary password on first login."
        );
    }
    
    /**
     * Tool: Check system operational status.
     * 
     * @param systemName The system to check
     * @return Formatted response
     */
    @Tool("Check the operational status of a system")
    public String checkSystemStatus(String systemName) {
        log.info("Checking status for system: {}", systemName);
        
        Map<String, Object> content = new HashMap<>();
        content.put("system", systemName);
        content.put("status", "operational");
        content.put("uptime", "99.9%");
        content.put("last_incident", "None in the last 30 days");
        
        return ResponseFormatter.formatMcpResponse(
                "System Status Check",
                content,
                String.format("System '%s' is operational with excellent uptime", systemName),
                null
        );
    }
}
