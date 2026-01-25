package com.bb.mcp.server.utils;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

/**
 * Date formatting utilities for MCP tools.
 * Mirrors the Python date_utils.py module.
 */
public class DateUtils {
    
    private static final DateTimeFormatter ISO_FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
    private static final DateTimeFormatter READABLE_FORMATTER = DateTimeFormatter.ofPattern("MMMM dd, yyyy HH:mm:ss");
    private static final DateTimeFormatter BR_FORMATTER = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
    
    /**
     * Get the current date in various formatted strings.
     * 
     * @return Map with different date formats
     */
    public static Map<String, String> getCurrentDateFormatted() {
        LocalDateTime now = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));
        
        Map<String, String> dateFormats = new HashMap<>();
        dateFormats.put("iso", now.format(ISO_FORMATTER));
        dateFormats.put("readable", now.format(READABLE_FORMATTER));
        dateFormats.put("br_format", now.format(BR_FORMATTER));
        dateFormats.put("timestamp", String.valueOf(now.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()));
        
        return dateFormats;
    }
    
    /**
     * Format a LocalDateTime in ISO format.
     * 
     * @param dateTime The datetime to format
     * @return ISO formatted string
     */
    public static String toIsoFormat(LocalDateTime dateTime) {
        return dateTime.format(ISO_FORMATTER);
    }
    
    /**
     * Format a LocalDateTime in readable format.
     * 
     * @param dateTime The datetime to format
     * @return Readable formatted string
     */
    public static String toReadableFormat(LocalDateTime dateTime) {
        return dateTime.format(READABLE_FORMATTER);
    }
    
    /**
     * Format a LocalDateTime in Brazilian format.
     * 
     * @param dateTime The datetime to format
     * @return Brazilian formatted string
     */
    public static String toBrazilianFormat(LocalDateTime dateTime) {
        return dateTime.format(BR_FORMATTER);
    }
}
