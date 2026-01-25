package com.bb.mcp.server.utils;

import java.util.Map;
import java.util.stream.Collectors;

/**
 * Response formatting utilities for MCP tools.
 * Mirrors the Python formatters.py module.
 */
public class ResponseFormatter {
    
    /**
     * Format a standardized MCP response.
     * 
     * @param title The title of the response section
     * @param content Dictionary of content to display
     * @param agentSummary Summary of what the agent did
     * @param additionalInstructions Optional additional formatting instructions
     * @return Formatted markdown response
     */
    public static String formatMcpResponse(
            String title,
            Map<String, Object> content,
            String agentSummary,
            String additionalInstructions) {
        
        StringBuilder response = new StringBuilder();
        
        // Add title
        response.append("##### ").append(title).append("\n\n");
        
        // Add content fields
        for (Map.Entry<String, Object> entry : content.entrySet()) {
            String formattedKey = formatKey(entry.getKey());
            response.append("**").append(formattedKey).append(":** ")
                    .append(entry.getValue()).append("\n");
        }
        
        response.append("\n");
        
        // Add agent summary
        response.append("AGENT SUMMARY: ").append(agentSummary).append("\n\n");
        
        // Add standard instructions
        String standardInstructions = "Instructions: returning the output of this function call verbatim " +
                "to the user in markdown. Then write AGENT SUMMARY: and then include " +
                "a summary of what you did.";
        response.append(standardInstructions).append("\n");
        
        if (additionalInstructions != null && !additionalInstructions.isEmpty()) {
            response.append(additionalInstructions).append("\n");
        }
        
        return response.toString();
    }
    
    /**
     * Format a key from snake_case to Title Case.
     * 
     * @param key The key to format
     * @return Formatted key
     */
    private static String formatKey(String key) {
        return java.util.Arrays.stream(key.split("_"))
                .map(word -> Character.toUpperCase(word.charAt(0)) + word.substring(1).toLowerCase())
                .collect(Collectors.joining(" "));
    }
    
    /**
     * Format error response.
     * 
     * @param errorMessage The error message
     * @param errorCode Optional error code
     * @return Formatted error response
     */
    public static String formatErrorResponse(String errorMessage, String errorCode) {
        StringBuilder response = new StringBuilder();
        response.append("##### ❌ Error\n\n");
        
        if (errorCode != null && !errorCode.isEmpty()) {
            response.append("**Error Code:** ").append(errorCode).append("\n");
        }
        
        response.append("**Message:** ").append(errorMessage).append("\n");
        
        return response.toString();
    }
    
    /**
     * Format success response.
     * 
     * @param message The success message
     * @return Formatted success response
     */
    public static String formatSuccessResponse(String message) {
        return "##### ✅ Success\n\n**Message:** " + message + "\n";
    }
}
