import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Message[] = [];
  userInput: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {}

  sendMessage() {
    if (!this.userInput.trim()) return;
    const userMsg = this.userInput;
    this.messages.push({ text: userMsg, sender: 'user' });
    this.userInput = '';

    this.http.post<any>('http://localhost:8000/chat', { message: userMsg }).subscribe(
      res => {
        this.messages.push({ text: res.reply, sender: 'bot' });
      },
      err => {
        this.messages.push({ text: "Sorry, there was an error.", sender: 'bot' });
      }
    );
  }
}