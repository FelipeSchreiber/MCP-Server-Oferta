package com.bb.mcp.server.utils;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for DateUtils.
 */
class DateUtilsTest {
    
    @Test
    void testGetCurrentDateFormatted() {
        Map<String, String> dateFormats = DateUtils.getCurrentDateFormatted();
        
        assertNotNull(dateFormats);
        assertNotNull(dateFormats.get("iso"));
        assertNotNull(dateFormats.get("readable"));
        assertNotNull(dateFormats.get("br_format"));
        assertNotNull(dateFormats.get("timestamp"));
        
        // Verify format patterns
        assertTrue(dateFormats.get("iso").matches("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.?\\d*"));
        assertTrue(dateFormats.get("br_format").matches("\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}:\\d{2}"));
    }
}
