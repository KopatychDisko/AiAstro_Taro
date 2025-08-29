#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { TarotServer } from "./tarot-server.js";
import { TarotHttpServer } from "./http-server.js";

/**
 * Parse command line arguments
 */
function parseArgs(): { transport: string; port: number } {
  const args = process.argv.slice(2);
  let transport = "stdio";
  let port = 3000;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--transport":
        transport = args[i + 1] || "stdio";
        i++;
        break;
      case "--port":
        port = parseInt(args[i + 1]) || 3000;
        i++;
        break;
      case "--help":
      case "-h":
        console.log(`
Tarot MCP Server

Usage: node dist/index.js [options]

Options:
  --transport <type>    Transport type: stdio, http, sse (default: stdio)
  --port <number>       Port for HTTP/SSE transport (default: 3000)
  --help, -h           Show this help message

Examples:
  node dist/index.js                           # Run with stdio transport
  node dist/index.js --transport http          # Run HTTP server on port 3000
  node dist/index.js --transport http --port 8080  # Run HTTP server on port 8080
        `);
        process.exit(0);
    }
  }

  return { transport, port };
}

/**
 * Main entry point for the Tarot MCP Server
 */
async function main() {
  const { transport, port } = parseArgs();

  console.error(`Starting Tarot MCP Server with ${transport} transport...`);

  // Asynchronously initialize the TarotServer
  const tarotServer = await TarotServer.create();
  console.error("Tarot card data loaded successfully.");

  if (transport === "http" || transport === "sse") {
    // Start HTTP server with the initialized TarotServer
    const httpServer = new TarotHttpServer(tarotServer, port);
    await httpServer.start();
  } else {
    // Start stdio server with the initialized TarotServer
    await startStdioServer(tarotServer);
  }
}

/**
 * Start the stdio-based MCP server
 */
async function startStdioServer(tarotServer: TarotServer) {
  const server = new Server(
    {
      name: "tarot-mcp-server",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // Handle tool listing
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: tarotServer.getAvailableTools(),
    };
  });

  // Handle tool execution
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      const result = await tarotServer.executeTool(name, args || {});
      return {
        content: [
          {
            type: "text",
            text: result,
          },
        ],
      };
    } catch (error) {
      return {
        isError: true,
        content: [
          {
            type: "text",
            text: `Error executing tool ${name}: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
      };
    }
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error("Tarot MCP Server running on stdio");
}

// Handle graceful shutdown
process.on("SIGINT", async () => {
  console.error("Shutting down Tarot MCP Server...");
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.error("Shutting down Tarot MCP Server...");
  process.exit(0);
});

// Start the server
main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});