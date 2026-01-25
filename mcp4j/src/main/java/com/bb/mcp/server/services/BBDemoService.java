package com.bb.mcp.server.services;

import com.bb.mcp.server.core.Domain;
import com.bb.mcp.server.core.MCPToolBase;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.agent.tool.ToolSpecification;
import jakarta.enterprise.context.ApplicationScoped;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Demo service with template tools for BB Internal Developer Platform.
 * Mirrors the Python BBDemoService class.
 */
@Slf4j
@ApplicationScoped
public class BBDemoService implements MCPToolBase {
    
    private final Domain domain = Domain.DEMO;
    private final int toolCount = 2; // add_two_numbers, get_user_info
    private final Map<String, java.util.function.Function<Object, Object>> tools = new HashMap<>();
    
    public BBDemoService() {
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
        // Register tool functions in the map
        tools.put("add_two_numbers", params -> {
            Map<String, Object> paramMap = (Map<String, Object>) params;
            int a = (Integer) paramMap.get("a");
            int b = (Integer) paramMap.get("b");
            return addTwoNumbers(a, b);
        });
        
        tools.put("get_user_info", params -> {
            Map<String, Object> paramMap = (Map<String, Object>) params;
            int userId = (Integer) paramMap.get("user_id");
            return getUserInfo(userId);
        });
        
        log.info("Registered {} tools for {} domain", toolCount, domain);
    }
    
    @Override
    public List<ToolSpecification> getToolSpecifications() {
        List<ToolSpecification> specs = new ArrayList<>();
        
        // Tool: add_two_numbers
        specs.add(ToolSpecification.builder()
                .name("add_two_numbers")
                .description("Adds two integer numbers together. Parameters: a (integer), b (integer)")
                .build());
        
        // Tool: get_user_info
        specs.add(ToolSpecification.builder()
                .name("get_user_info")
                .description("Retrieves user information by user_id. Returns user profile " +
                        "including id, name, and status. This tool accesses sensitive user data. " +
                        "Parameters: user_id (integer)")
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
     * Tool: Basic arithmetic operation.
     * Adds two integer numbers together.
     * 
     * @param a First number
     * @param b Second number
     * @return Sum of a and b
     */
    @Tool("Adds two integer numbers together")
    public int addTwoNumbers(int a, int b) {
        log.debug("Adding {} + {} = {}", a, b, a + b);
        return a + b;
    }
    
    /**
     * Tool: Access user information.
     * Retrieves user information by user_id.
     * 
     * @param userId The user ID
     * @return User information map
     */
    @Tool("Retrieves user information by user_id. Returns user profile including id, name, and status.")
    public Map<String, Object> getUserInfo(int userId) {
        log.debug("Retrieving user info for user_id: {}", userId);
        
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("id", userId);
        userInfo.put("name", "User " + userId);
        userInfo.put("status", "active");
        userInfo.put("cpf", String.format("000.000.000-0%d", userId));
        userInfo.put("email", String.format("user%d@bb.com.br", userId));
        
        return userInfo;
    }
    
    /**
     * Resource: Application configuration.
     * Provides the application configuration.
     * 
     * @return Configuration map
     */
    public Map<String, Object> getAppConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("theme", "dark");
        config.put("version", "1.2");
        return config;
    }
    
    /**
     * Resource: User telephone with path parameters.
     * Retrieves a user's telephone by ID.
     * 
     * @param userId The user ID
     * @return User telephone information
     */
    public Map<String, Object> getUserTelephone(int userId) {
        Map<String, Object> telephone = new HashMap<>();
        telephone.put("id", userId);
        telephone.put("name", "User " + userId);
        telephone.put("telephone", String.format("+55-61-3000-%04d", userId));
        return telephone;
    }
}
