package com.bb.mcp.server.core;

import jakarta.enterprise.context.ApplicationScoped;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.Map;

/**
 * Factory for creating and managing MCP tools.
 * Mirrors the Python MCPToolFactory class.
 */
@Slf4j
@ApplicationScoped
public class MCPToolFactory {
    
    private final Map<Domain, MCPToolBase> services = new HashMap<>();
    
    /**
     * Register a tool service with the factory.
     * 
     * @param service The service to register
     */
    public void registerService(MCPToolBase service) {
        services.put(service.getDomain(), service);
        log.info("✅ Registered service: {} with {} tools", 
                service.getDomain(), service.getToolCount());
    }
    
    /**
     * Get a service by domain.
     * 
     * @param domain The domain to look up
     * @return The service or null if not found
     */
    public MCPToolBase getService(Domain domain) {
        return services.get(domain);
    }
    
    /**
     * Get all registered services.
     * 
     * @return Map of all services
     */
    public Map<Domain, MCPToolBase> getAllServices() {
        return new HashMap<>(services);
    }
    
    /**
     * Get a summary of all tools and services.
     * 
     * @return ToolSummary object
     */
    public ToolSummary getToolSummary() {
        ToolSummary summary = new ToolSummary();
        summary.setTotalServices(services.size());
        
        int totalTools = 0;
        Map<String, ServiceInfo> serviceDetails = new HashMap<>();
        
        for (Map.Entry<Domain, MCPToolBase> entry : services.entrySet()) {
            Domain domain = entry.getKey();
            MCPToolBase service = entry.getValue();
            int toolCount = service.getToolCount();
            totalTools += toolCount;
            
            ServiceInfo info = new ServiceInfo();
            info.setToolCount(toolCount);
            info.setClassName(service.getClass().getSimpleName());
            serviceDetails.put(domain.getValue(), info);
        }
        
        summary.setTotalTools(totalTools);
        summary.setServices(serviceDetails);
        
        return summary;
    }
    
    /**
     * Log server initialization info.
     * 
     * @param serverName The name of the server
     * @param enableAuth Whether authentication is enabled
     */
    public void logServerInfo(String serverName, boolean enableAuth) {
        ToolSummary summary = getToolSummary();
        
        log.info("🚀 {} initialized", serverName);
        log.info("📊 Total services: {}", summary.getTotalServices());
        log.info("🔧 Total tools: {}", summary.getTotalTools());
        log.info("🔐 Authentication: {}", enableAuth ? "Enabled" : "Disabled");
        
        for (Map.Entry<String, ServiceInfo> entry : summary.getServices().entrySet()) {
            String domain = entry.getKey();
            ServiceInfo info = entry.getValue();
            log.info("   📁 {}: {} tools ({})", domain, info.getToolCount(), info.getClassName());
        }
    }
    
    /**
     * Tool summary data class.
     */
    @lombok.Data
    public static class ToolSummary {
        private int totalServices;
        private int totalTools;
        private Map<String, ServiceInfo> services;
    }
    
    /**
     * Service info data class.
     */
    @lombok.Data
    public static class ServiceInfo {
        private int toolCount;
        private String className;
    }
}
