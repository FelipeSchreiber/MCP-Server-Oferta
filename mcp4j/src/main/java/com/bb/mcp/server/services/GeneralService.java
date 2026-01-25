package com.bb.mcp.server.services;

import com.bb.mcp.server.core.Domain;
import com.bb.mcp.server.core.MCPToolBase;
import com.bb.mcp.server.utils.DateUtils;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.agent.tool.ToolSpecification;
import jakarta.enterprise.context.ApplicationScoped;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * General service with utility tools.
 * Mirrors the Python GeneralService class.
 */
@Slf4j
@ApplicationScoped
public class GeneralService implements MCPToolBase {
    
    private final Domain domain = Domain.GENERAL;
    private final int toolCount = 2; // get_current_date, format_text
    private final Map<String, java.util.function.Function<Object, Object>> tools = new HashMap<>();
    
    public GeneralService() {
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
        tools.put("get_current_date", params -> getCurrentDate());
        
        tools.put("format_text", params -> {
            Map<String, Object> paramMap = (Map<String, Object>) params;
            String text = (String) paramMap.get("text");
            String format = (String) paramMap.get("format");
            return formatText(text, format);
        });
        
        log.info("Registered {} tools for {} domain", toolCount, domain);
    }
    
    @Override
    public List<ToolSpecification> getToolSpecifications() {
        List<ToolSpecification> specs = new ArrayList<>();
        
        specs.add(ToolSpecification.builder()
                .name("get_current_date")
                .description("Get the current date in formatted strings. No parameters required.")
                .build());
        
        specs.add(ToolSpecification.builder()
                .name("format_text")
                .description("Format text in various styles (uppercase, lowercase, title). " +
                        "Parameters: text (string), format (string - uppercase, lowercase, or title)")
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
     * Tool: Get current date.
     * 
     * @return Map with formatted date strings
     */
    @Tool("Get the current date in formatted strings")
    public Map<String, String> getCurrentDate() {
        log.debug("Getting current date");
        return DateUtils.getCurrentDateFormatted();
    }
    
    /**
     * Tool: Format text.
     * 
     * @param text The text to format
     * @param format The format style
     * @return Formatted text
     */
    @Tool("Format text in various styles (uppercase, lowercase, title)")
    public String formatText(String text, String format) {
        log.debug("Formatting text: {} with format: {}", text, format);
        
        switch (format.toLowerCase()) {
            case "uppercase":
                return text.toUpperCase();
            case "lowercase":
                return text.toLowerCase();
            case "title":
                return toTitleCase(text);
            default:
                return text;
        }
    }
    
    /**
     * Convert text to title case.
     * 
     * @param text The text to convert
     * @return Title case text
     */
    private String toTitleCase(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        
        String[] words = text.split("\\s+");
        StringBuilder titleCase = new StringBuilder();
        
        for (String word : words) {
            if (word.length() > 0) {
                titleCase.append(Character.toUpperCase(word.charAt(0)))
                        .append(word.substring(1).toLowerCase())
                        .append(" ");
            }
        }
        
        return titleCase.toString().trim();
    }
}
