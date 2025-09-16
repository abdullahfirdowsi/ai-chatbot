import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { firstValueFrom } from 'rxjs';
import { RagService, KnowledgeBaseStats } from '../services/rag.service';

interface DocumentResult {
  content: string;
  metadata: any;
  source: string;
}

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    MatButtonModule, 
    MatIconModule, 
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatChipsModule
  ],
  templateUrl: './documents.component.html',
  styleUrls: ['./documents.component.css']
})
export class DocumentsComponent implements OnInit {
  private readonly API_BASE_URL = 'http://localhost:8000';
  
  // Upload state
  selectedFile: File | null = null;
  isUploading = false;
  uploadProgress = 0;
  
  // Search state
  searchQuery = '';
  searchResults: DocumentResult[] = [];
  isSearching = false;
  
  // Knowledge base stats
  stats: KnowledgeBaseStats | null = null;
  isLoadingStats = false;
  
  // Test query state
  testQuery = '';
  testResult: any = null;
  isTestingQuery = false;
  
  // Supported formats
  supportedFormats = [
    { ext: '.pdf', desc: 'PDF Documents' },
    { ext: '.txt', desc: 'Text Files' },
    { ext: '.docx', desc: 'Word Documents' },
    { ext: '.md', desc: 'Markdown Files' }
  ];

  get acceptedFileFormats(): string {
    return this.supportedFormats.map(f => f.ext).join(',');
  }

  @ViewChild('fileInputRef') fileInputRef!: ElementRef<HTMLInputElement>;

  constructor(private http: HttpClient, private snackBar: MatSnackBar, private ragService: RagService) {}

  ngOnInit(): void {
    this.loadStats();
  }

  openFileSelector(): void {
    this.fileInputRef.nativeElement.click();
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      const supportedExtensions = this.supportedFormats.map(f => f.ext);
      
      if (!supportedExtensions.includes(fileExtension)) {
        this.snackBar.open(
          `Unsupported file type. Supported formats: ${supportedExtensions.join(', ')}`,
          'Close',
          { duration: 4000, panelClass: ['error-snackbar'] }
        );
        return;
      }
      
      // Check file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        this.snackBar.open('File too large. Maximum size is 10MB.', 'Close', {
          duration: 4000,
          panelClass: ['error-snackbar']
        });
        return;
      }
      
      this.selectedFile = file;
    }
  }

  async uploadDocument(): Promise<void> {
    if (!this.selectedFile) return;

    this.isUploading = true;
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('title', this.selectedFile.name);

    try {
      const response = await firstValueFrom(this.http.post<any>(
        `${this.API_BASE_URL}/documents/upload`,
        formData
      ));

      this.snackBar.open(
        `Successfully uploaded ${this.selectedFile.name}! Created ${response.chunks_created} chunks.`,
        'Close',
        { duration: 4000, panelClass: ['success-snackbar'] }
      );

      // Reset form
      this.selectedFile = null;
      if (this.fileInputRef) {
        this.fileInputRef.nativeElement.value = '';
      }
      
      // Refresh stats and notify service
      this.loadStats();
      this.ragService.notifyKnowledgeBaseUpdated();

    } catch (error: any) {
      console.error('Upload error:', error);
      this.snackBar.open(
        error.error?.detail || 'Failed to upload document',
        'Close',
        { duration: 4000, panelClass: ['error-snackbar'] }
      );
    } finally {
      this.isUploading = false;
    }
  }

  async searchDocuments(): Promise<void> {
    if (!this.searchQuery.trim()) return;

    this.isSearching = true;
    this.searchResults = [];

    try {
      const response = await firstValueFrom(this.http.get<any>(
        `${this.API_BASE_URL}/documents/search?query=${encodeURIComponent(this.searchQuery)}&limit=10`
      ));

      this.searchResults = response.results || [];
      
      if (this.searchResults.length === 0) {
        this.snackBar.open('No relevant documents found.', 'Close', {
          duration: 3000
        });
      }

    } catch (error: any) {
      console.error('Search error:', error);
      this.snackBar.open('Search failed. Please try again.', 'Close', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isSearching = false;
    }
  }

  async testRAGQuery(): Promise<void> {
    if (!this.testQuery.trim()) return;

    this.isTestingQuery = true;
    this.testResult = null;

    try {
      const formData = new FormData();
      formData.append('query', this.testQuery);
      formData.append('use_context', 'true');

      const response = await firstValueFrom(this.http.post<any>(
        `${this.API_BASE_URL}/documents/test-query`,
        formData
      ));

      this.testResult = response;

    } catch (error: any) {
      console.error('Test query error:', error);
      this.snackBar.open('Test query failed. Please try again.', 'Close', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isTestingQuery = false;
    }
  }

  async loadStats(): Promise<void> {
    this.isLoadingStats = true;

    try {
      const response = await firstValueFrom(this.http.get<any>(
        `${this.API_BASE_URL}/documents/stats`
      ));

      this.stats = response.stats;

    } catch (error: any) {
      console.error('Stats error:', error);
      this.snackBar.open('Failed to load knowledge base stats.', 'Close', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isLoadingStats = false;
    }
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  truncateText(text: string, maxLength: number = 200): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }

  clearSearch(): void {
    this.searchQuery = '';
    this.searchResults = [];
  }

  clearTestResult(): void {
    this.testQuery = '';
    this.testResult = null;
  }
}
