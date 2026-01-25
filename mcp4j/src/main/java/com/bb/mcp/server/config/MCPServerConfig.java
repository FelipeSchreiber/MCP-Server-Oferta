package com.bb.mcp.server.config;

import io.smallrye.config.ConfigMapping;
import io.smallrye.config.WithDefault;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

/**
 * MCP Server configuration settings.
 * Mirrors the Python settings.py structure.
 */
@ApplicationScoped
@ConfigMapping(prefix = "mcp.server")
public interface MCPServerConfig {
    
    // Server settings
    @WithDefault("0.0.0.0")
    String host();
    
    @WithDefault("9000")
    Integer port();
    
    @WithDefault("false")
    Boolean debug();
    
    @WithDefault("BBMCPServer")
    String name();
    
    @WithDefault("1.0.0")
    String version();
    
    @WithDefault("Java-based MCP Server with Quarkus and LangChain4j")
    String description();
    
    @WithDefault("false")
    Boolean enableAuth();
    
    // Authentication settings
    Auth auth();
    
    interface Auth {
        Optional<String> tenantId();
        Optional<String> clientId();
        Optional<String> jwksUri();
        Optional<String> issuer();
        Optional<String> audience();
    }
}

