package com.bb.mcp.server;

import com.bb.mcp.server.core.MCPToolFactory;
import com.bb.mcp.server.services.BBDemoService;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Integration tests for MCP Server Application.
 */
@QuarkusTest
class MCPServerApplicationTests {
    
    @Inject
    MCPToolFactory factory;
    
    @Inject
    BBDemoService bbDemoService;
    
    @Test
    void contextLoads() {
        assertNotNull(factory);
        assertNotNull(bbDemoService);
    }
    
    @Test
    void testServiceRegistration() {
        assertNotNull(factory.getAllServices());
        assertTrue(factory.getAllServices().size() > 0);
    }
    
    @Test
    void testToolSummary() {
        MCPToolFactory.ToolSummary summary = factory.getToolSummary();
        assertNotNull(summary);
        assertTrue(summary.getTotalServices() > 0);
        assertTrue(summary.getTotalTools() > 0);
    }
}

