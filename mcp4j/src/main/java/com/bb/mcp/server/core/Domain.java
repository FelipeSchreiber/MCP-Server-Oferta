package com.bb.mcp.server.core;

/**
 * Service domains for organizing MCP tools.
 * Mirrors the Python Domain enum.
 */
public enum Domain {
    TECH_SUPPORT("tech_support"),
    GENERAL("general"),
    DATA("data"),
    DEMO("demo");
    
    private final String value;
    
    Domain(String value) {
        this.value = value;
    }
    
    public String getValue() {
        return value;
    }
    
    @Override
    public String toString() {
        return value;
    }
}
