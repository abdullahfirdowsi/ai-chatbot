import { Component, OnInit, ElementRef, ViewChild, AfterViewChecked, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { RagService } from '../services/rag.service';
import { Subscription } from 'rxjs';
import { environment } from '../../environments/environment';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  id: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatIconModule, MatSnackBarModule, MatTooltipModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, OnDestroy {
  messages: Message[] = [];
  userInput: string = '';
  isLoading: boolean = false;
  isKnowledgeBaseAvailable = false;
  private subscription?: Subscription;
  private readonly API_BASE_URL = environment.apiUrl;

  constructor(
    private http: HttpClient, 
    private snackBar: MatSnackBar, 
    private sanitizer: DomSanitizer,
    private ragService: RagService
  ) {}

  ngOnInit(): void {
    // Subscribe to knowledge base availability
    this.subscription = this.ragService.knowledgeBaseAvailable$.subscribe(
      isAvailable => {
        this.isKnowledgeBaseAvailable = isAvailable;
      }
    );
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  async sendMessage() {
    if (!this.userInput.trim() || this.isLoading) return;
    
    const userMsg = this.userInput.trim();
    this.messages.push({ 
      text: userMsg, 
      sender: 'user',
      timestamp: new Date(),
      id: this.generateId()
    });
    this.userInput = '';
    this.isLoading = true;
    
    // Immediately scroll to show the user's message
    this.scrollToBottom();

    try {
      const response = await this.ragService.sendChatMessage(userMsg);
      
      // Handle different response formats from different endpoints
      const botReply = response.response || response.reply || response.answer || 'No response received';
      
      this.messages.push({ 
        text: botReply, 
        sender: 'bot',
        timestamp: new Date(),
        id: this.generateId()
      });
      
      this.isLoading = false;
      this.scrollToBottom();
    } catch (error: any) {
      console.error('Chat error:', error);
      this.messages.push({ 
        text: "Sorry, I encountered an error. Please try again.", 
        sender: 'bot',
        timestamp: new Date(),
        id: this.generateId()
      });
      this.isLoading = false;
      
      const errorMessage = error.error?.detail || 'Connection error. Please check if the server is running.';
      this.snackBar.open(errorMessage, 'Close', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
    }
  }

  clearConversation() {
    if (this.isLoading) return;
    
    this.isLoading = true;
    
    this.http.delete<any>(`${this.API_BASE_URL}/chat/clear`).subscribe({
      next: (res) => {
        this.messages = [];
        this.isLoading = false;
        this.snackBar.open('Conversation cleared!', 'Close', {
          duration: 2000,
          panelClass: ['success-snackbar']
        });
      },
      error: (err) => {
        console.error('Clear conversation error:', err);
        // Still clear the frontend messages even if backend fails
        this.messages = [];
        this.isLoading = false;
        this.snackBar.open('Conversation cleared locally', 'Close', {
          duration: 2000
        });
      }
    });
  }

  getSuggestedQuestions(): string[] {
    return [
      'What can you help me with?',
      'Tell me about artificial intelligence',
      'How do you work?',
      'What are your capabilities?'
    ];
  }

  trackByMessageId(index: number, message: Message): string {
    return message.id;
  }

  formatTime(timestamp: Date): string {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(timestamp);
  }

  private generateId(): string {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }


  private scrollToBottom() {
    // Small delay to ensure DOM is updated and new message is rendered
    setTimeout(() => {
      const messagesContainer = document.querySelector('.messages-container');
      if (messagesContainer) {
        // Scroll to the very bottom with smooth behavior
        messagesContainer.scrollTo({
          top: messagesContainer.scrollHeight,
          behavior: 'smooth'
        });
      }
    }, 150);
  }

  // Simple markdown parser for basic formatting
  parseMarkdown(text: string): SafeHtml {
    if (!text) return this.sanitizer.bypassSecurityTrustHtml('');
    
    let html = text
      // Convert **bold** to <strong> first (process bold before italic)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      // Convert `code` to <code>
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // Convert remaining *italic* to <em> (after bold is processed)
      .replace(/\*([^*<>]+)\*/g, '<em>$1</em>')
      // Convert bullet points at start of line
      .replace(/^\* (.+)$/gm, '|||LIST_ITEM|||$1|||END_LIST_ITEM|||')
      // Convert numbered lists
      .replace(/^\d+\. (.+)$/gm, '|||LIST_ITEM|||$1|||END_LIST_ITEM|||')
      // Convert line breaks
      .replace(/\n/g, '<br>');
    
    // Process list items
    const listItems = html.match(/(\|\|\|LIST_ITEM\|\|\|[^|]+\|\|\|END_LIST_ITEM\|\|\|(?:<br>)?)+/g);
    if (listItems) {
      listItems.forEach(listGroup => {
        const items = listGroup
          .replace(/\|\|\|LIST_ITEM\|\|\|/g, '<li>')
          .replace(/\|\|\|END_LIST_ITEM\|\|\|/g, '</li>')
          .replace(/<br>/g, '');
        html = html.replace(listGroup, '<ul>' + items + '</ul>');
      });
    }
    
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
