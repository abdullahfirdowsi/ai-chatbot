import { Component, signal } from '@angular/core';
import { ChatComponent } from './chat/chat.component';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChatComponent, MatIconModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class App {
  protected readonly title = signal('AI Chatbot');

  onLogoLoad(event: any) {
    // Logo loaded successfully, hide fallback
    const fallback = event.target.parentElement.querySelector('.fallback-icon');
    if (fallback) {
      fallback.style.display = 'none';
    }
  }

  onLogoError(event: any) {
    // Hide the broken image and show the fallback
    event.target.style.display = 'none';
    const fallback = event.target.parentElement.querySelector('.fallback-icon');
    if (fallback) {
      fallback.style.display = 'flex';
    }
  }
}
