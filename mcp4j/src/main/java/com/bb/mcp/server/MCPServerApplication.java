package com.bb.mcp.server;

import com.bb.mcp.server.config.MCPServerConfig;
import com.bb.mcp.server.core.MCPToolFactory;
import com.bb.mcp.server.services.BBDemoService;
import com.bb.mcp.server.services.GeneralService;
import com.bb.mcp.server.services.TechSupportService;
import io.quarkus.runtime.Quarkus;
import io.quarkus.runtime.QuarkusApplication;
import io.quarkus.runtime.annotations.QuarkusMain;
import jakarta.inject.Inject;
import lombok.extern.slf4j.Slf4j;

/**
 * BB MCP Server - Java-based MCP server with LangChain4j and Quarkus.
 * Mirrors the Python mcp_server.py implementation.
 */
@Slf4j
@QuarkusMain
public class MCPServerApplication implements QuarkusApplication {
    
    @Inject
    MCPServerConfig config;
    
    @Inject
    MCPToolFactory factory;
    
    @Inject
    BBDemoService bbDemoService;
    
    @Inject
    TechSupportService techSupportService;
    
    @Inject
    GeneralService generalService;
    
    public static void main(String[] args) {
        Quarkus.run(MCPServerApplication.class, args);
    }
    
    @Override
    public int run(String... args) {
        log.info("🚀 Initializing BB MCP4J Server...");
        
        // Register services with the factory
        factory.registerService(bbDemoService);
        factory.registerService(techSupportService);
        factory.registerService(generalService);
        
        // Log server information
        factory.logServerInfo(config.name(), config.enableAuth());
        
        log.info("✅ BB MCP4J Server initialized successfully");
        log.info("🌐 Server listening on {}:{}", config.host(), config.port());
        
        Quarkus.waitForExit();
        return 0;
    }
}

