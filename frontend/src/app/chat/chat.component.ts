import { Component, OnInit, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';

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
export class ChatComponent implements OnInit {
  messages: Message[] = [];
  userInput: string = '';
  isLoading: boolean = false;
  private readonly API_BASE_URL = 'http://localhost:8000';

  constructor(private http: HttpClient, private snackBar: MatSnackBar) {}

  ngOnInit(): void {}

  sendMessage() {
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

    this.http.post<any>(`${this.API_BASE_URL}/chat`, { message: userMsg }).subscribe({
      next: (res) => {
        this.messages.push({ 
          text: res.reply, 
          sender: 'bot',
          timestamp: new Date(),
          id: this.generateId()
        });
        this.isLoading = false;
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Chat error:', err);
        this.messages.push({ 
          text: "Sorry, I encountered an error. Please try again.", 
          sender: 'bot',
          timestamp: new Date(),
          id: this.generateId()
        });
        this.isLoading = false;
        this.snackBar.open('Connection error. Please check if the server is running.', 'Close', {
          duration: 3000,
          panelClass: ['error-snackbar']
        });
      }
    });
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
    // Small delay to ensure DOM is updated
    setTimeout(() => {
      const messagesContainer = document.querySelector('.messages-container');
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }
    }, 100);
  }
}