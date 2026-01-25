package com.bb.mcp.server.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for BBDemoService.
 */
class BBDemoServiceTest {
    
    private BBDemoService service;
    
    @BeforeEach
    void setUp() {
        service = new BBDemoService();
    }
    
    @Test
    void testAddTwoNumbers() {
        int result = service.addTwoNumbers(5, 3);
        assertEquals(8, result);
    }
    
    @Test
    void testAddTwoNumbersNegative() {
        int result = service.addTwoNumbers(-5, 3);
        assertEquals(-2, result);
    }
    
    @Test
    void testGetUserInfo() {
        Map<String, Object> userInfo = service.getUserInfo(1234);
        
        assertNotNull(userInfo);
        assertEquals(1234, userInfo.get("id"));
        assertEquals("User 1234", userInfo.get("name"));
        assertEquals("active", userInfo.get("status"));
        assertTrue(((String) userInfo.get("email")).contains("@bb.com.br"));
    }
    
    @Test
    void testGetAppConfig() {
        Map<String, Object> config = service.getAppConfig();
        
        assertNotNull(config);
        assertEquals("dark", config.get("theme"));
        assertEquals("1.2", config.get("version"));
    }
    
    @Test
    void testGetUserTelephone() {
        Map<String, Object> telephone = service.getUserTelephone(1234);
        
        assertNotNull(telephone);
        assertEquals(1234, telephone.get("id"));
        assertTrue(((String) telephone.get("telephone")).startsWith("+55-61-3000-"));
    }
    
    @Test
    void testToolCount() {
        assertEquals(2, service.getToolCount());
    }
}
