package com.example.christian.computer_stats_app;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseUtils {
    public static Connection getConnection() throws SQLException {
        // db parameters
        String url       = "jdbc:mysql://localhost:8889/computer-stats";
        String user      = "computer-stats";
        String password  = "ouaGS1zjUeu5sW3x";

        Connection conn = null;
        conn = DriverManager.getConnection(url, user, password);
        return conn;
    }
}