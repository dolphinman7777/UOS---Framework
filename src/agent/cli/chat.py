#!/usr/bin/env python3

import sys
import os
import argparse
import logging
from typing import Optional
from datetime import datetime

from ...agent.context.conversation_manager import ConversationManager

class JeffCLI:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.conversation = ConversationManager()
        
        # CLI state
        self.debug_mode = False
        self.show_context = False
        self.user_id = "cli_user"
        
    def print_banner(self):
        banner = """
==========================================
             JEFF CLI v1.0                
==========================================
Commands:
  /debug    - Toggle debug mode
  /context  - Show conversation context
  /clear    - Clear conversation history
  /help     - Show this help message
  /exit     - Exit the chat
"""
        print(banner)
        
    def handle_command(self, command: str) -> bool:
        """Handle CLI commands. Returns True if should continue."""
        if command == "/exit":
            return False
        elif command == "/debug":
            self.debug_mode = not self.debug_mode
            print(f"Debug mode: {'on' if self.debug_mode else 'off'}")
        elif command == "/context":
            self.show_context = not self.show_context
            print(f"Context display: {'on' if self.show_context else 'off'}")
        elif command == "/clear":
            self.conversation.clear_conversation(self.user_id)
            print("Conversation history cleared")
        elif command == "/help":
            self.print_banner()
        else:
            print(f"Unknown command: {command}")
        return True
        
    def chat_loop(self):
        """Main chat loop"""
        self.print_banner()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle commands
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # Get context if enabled
                if self.show_context:
                    context = self.conversation.get_context(self.user_id, user_input)
                    if context:
                        print("\nContext:")
                        print(context)
                        print()
                
                # Generate response
                response = self.conversation.generate_response(self.user_id, user_input)
                
                # Print response
                print(f"\nJEFF: {response}\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                self.logger.error(f"Error in chat loop: {str(e)}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                print("\nSorry, I encountered an error. Please try again.")

def main():
    parser = argparse.ArgumentParser(description='JEFF CLI')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--context', action='store_true', help='Show conversation context')
    args = parser.parse_args()
    
    cli = JeffCLI()
    cli.debug_mode = args.debug
    cli.show_context = args.context
    cli.chat_loop()

if __name__ == "__main__":
    main() 