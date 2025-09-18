import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, firstValueFrom } from 'rxjs';
import { environment } from '../../environments/environment';

export interface KnowledgeBaseStats {
  total_documents: number;
  embedding_dimension: number;
  persist_directory: string;
}

@Injectable({
  providedIn: 'root'
})
export class RagService {
  private readonly API_BASE_URL = environment.apiUrl;
  private knowledgeBaseAvailable = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {
    this.checkKnowledgeBaseStatus();
  }

  get knowledgeBaseAvailable$(): Observable<boolean> {
    return this.knowledgeBaseAvailable.asObservable();
  }

  get isKnowledgeBaseAvailable(): boolean {
    return this.knowledgeBaseAvailable.value;
  }

  async checkKnowledgeBaseStatus(): Promise<void> {
    try {
      const response = await firstValueFrom(this.http.get<any>(`${this.API_BASE_URL}/documents/stats`));
      const hasDocuments = response.stats && response.stats.total_documents > 0;
      this.knowledgeBaseAvailable.next(hasDocuments);
    } catch (error) {
      console.error('Error checking knowledge base status:', error);
      this.knowledgeBaseAvailable.next(false);
    }
  }

  async sendChatMessage(message: string): Promise<any> {
    const endpoint = this.isKnowledgeBaseAvailable ? '/chat/rag' : '/chat';
    
    try {
      const response = await firstValueFrom(this.http.post<any>(
        `${this.API_BASE_URL}${endpoint}`,
        { message, query: message } // Some endpoints expect 'query' instead of 'message'
      ));
      return response;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }

  async getKnowledgeBaseStats(): Promise<KnowledgeBaseStats | null> {
    try {
      const response = await firstValueFrom(this.http.get<any>(`${this.API_BASE_URL}/documents/stats`));
      return response.stats;
    } catch (error) {
      console.error('Error getting knowledge base stats:', error);
      return null;
    }
  }

  notifyKnowledgeBaseUpdated(): void {
    this.checkKnowledgeBaseStatus();
  }
}
