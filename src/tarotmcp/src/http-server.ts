import express from 'express';
import cors from 'cors';
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { TarotServer } from "./tarot-server.js";

/**
 * HTTP Server for Tarot MCP with SSE (Server-Sent Events) support
 */
export class TarotHttpServer {
  private app: express.Application;
  private server: Server;
  private tarotServer: TarotServer;
  private port: number;

  constructor(tarotServer: TarotServer, port: number = 3000) {
    this.port = port;
    this.app = express();
    this.tarotServer = tarotServer;
    
    // Create MCP server instance
    this.server = new Server(
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

    this.setupMiddleware();
    this.setupMCPHandlers();
    this.setupRoutes();
  }

  /**
   * Setup Express middleware
   */
  private setupMiddleware(): void {
    this.app.use(cors());
    this.app.use(express.json());
  }

  /**
   * Setup MCP request handlers
   */
  private setupMCPHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: this.tarotServer.getAvailableTools(),
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      try {
        const result = await this.tarotServer.executeTool(name, args || {});
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
  }

  /**
   * Setup HTTP routes
   */
  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        endpoints: {
          sse: '/sse',
          mcp: '/mcp',
          health: '/health',
          api: {
            reading: '/api/reading',
            customSpread: '/api/custom-spread',
            info: '/api/info'
          }
        }
      });
    });

    // API info endpoint
    this.app.get('/api/info', (req, res) => {
      res.json({
        name: 'Tarot MCP Server',
        version: '1.0.0',
        capabilities: ['tools'],
        tools: this.tarotServer.getAvailableTools(),
        endpoints: {
          sse: '/sse',
          mcp: '/mcp',
          health: '/health'
        }
      });
    });

    // SSE endpoint for MCP
    this.app.get('/sse', async (req, res) => {
      try {
        console.log('SSE connection request received');
        const transport = new SSEServerTransport('/sse', res);
        await this.server.connect(transport);
        console.log('SSE connection established');
      } catch (error) {
        console.error('SSE connection error:', error);
        res.status(500).json({ error: 'Failed to establish SSE connection' });
      }
    });

    // MCP HTTP endpoint (alternative to SSE)
    this.app.post('/mcp', async (req, res) => {
      try {
        // This would need proper MCP HTTP transport implementation
        res.json({ message: 'MCP HTTP endpoint - not yet implemented' });
      } catch (error) {
        res.status(500).json({ error: error instanceof Error ? error.message : String(error) });
      }
    });

    // Example of a direct API endpoint
    this.app.post('/api/reading', async (req, res) => {
      try {
        const { spreadType, question, sessionId } = req.body;
        const result = await this.tarotServer.executeTool('perform_reading', { spreadType, question, sessionId });
        res.json({ result });
      } catch (error) {
        res.status(500).json({ error: error instanceof Error ? error.message : String(error) });
      }
    });

    // Custom spread creation endpoint
    this.app.post('/api/custom-spread', async (req, res) => {
      try {
        const { spreadName, description, positions, question, sessionId } = req.body;
        const result = await this.tarotServer.executeTool('create_custom_spread', {
          spreadName,
          description,
          positions,
          question,
          sessionId
        });
        res.json({ result });
      } catch (error) {
        res.status(500).json({ error: error instanceof Error ? error.message : String(error) });
      }
    });
  }

  /**
   * Start the HTTP server
   */
  public async start(): Promise<void> {
    return new Promise((resolve) => {
      this.app.listen(this.port, '0.0.0.0', () => {
        console.log(`🔮 Tarot MCP Server running on http://0.0.0.0:${this.port}`);
        console.log(`📡 SSE endpoint: http://0.0.0.0:${this.port}/sse`);
        console.log(`🔧 MCP endpoint: http://0.0.0.0:${this.port}/mcp`);
        console.log(`❤️  Health check: http://0.0.0.0:${this.port}/health`);
        console.log(`📋 API info: http://0.0.0.0:${this.port}/api/info`);
        resolve();
      });
    });
  }
}