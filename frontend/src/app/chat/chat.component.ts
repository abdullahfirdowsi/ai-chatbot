import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatIconModule, MatSnackBarModule],
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
    this.messages.push({ text: userMsg, sender: 'user' });
    this.userInput = '';
    this.isLoading = true;

    this.http.post<any>(`${this.API_BASE_URL}/chat`, { message: userMsg }).subscribe({
      next: (res) => {
        this.messages.push({ text: res.reply, sender: 'bot' });
        this.isLoading = false;
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Chat error:', err);
        this.messages.push({ 
          text: "Sorry, I encountered an error. Please try again.", 
          sender: 'bot' 
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

  private scrollToBottom() {
    // Small delay to ensure DOM is updated
    setTimeout(() => {
      const chatBody = document.querySelector('.chat-body');
      if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    }, 100);
  }
}