import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { ChatComponent } from './chat/chat.component';
import { DocumentsComponent } from './documents/documents.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, MatTabsModule, MatIconModule, ChatComponent, DocumentsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class App {
  protected readonly title = signal('AI Chatbot');
}
