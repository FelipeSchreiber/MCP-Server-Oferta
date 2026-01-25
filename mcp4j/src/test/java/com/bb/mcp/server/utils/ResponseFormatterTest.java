package com.bb.mcp.server.utils;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for ResponseFormatter.
 */
class ResponseFormatterTest {
    
    @Test
    void testFormatMcpResponse() {
        Map<String, Object> content = new HashMap<>();
        content.put("user_name", "John Doe");
        content.put("status_code", 200);
        
        String response = ResponseFormatter.formatMcpResponse(
                "Test Result",
                content,
                "Successfully processed request",
                "Additional info here"
        );
        
        assertNotNull(response);
        assertTrue(response.contains("##### Test Result"));
        assertTrue(response.contains("**User Name:** John Doe"));
        assertTrue(response.contains("**Status Code:** 200"));
        assertTrue(response.contains("AGENT SUMMARY: Successfully processed request"));
        assertTrue(response.contains("Additional info here"));
    }
    
    @Test
    void testFormatErrorResponse() {
        String response = ResponseFormatter.formatErrorResponse(
                "Something went wrong",
                "ERR_500"
        );
        
        assertNotNull(response);
        assertTrue(response.contains("##### ❌ Error"));
        assertTrue(response.contains("**Error Code:** ERR_500"));
        assertTrue(response.contains("**Message:** Something went wrong"));
    }
    
    @Test
    void testFormatSuccessResponse() {
        String response = ResponseFormatter.formatSuccessResponse("Operation completed");
        
        assertNotNull(response);
        assertTrue(response.contains("##### ✅ Success"));
        assertTrue(response.contains("**Message:** Operation completed"));
    }
}
