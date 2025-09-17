# Deployment Guide: Backend on Render & Frontend on Vercel

This guide will help you deploy your AI Tutor Chatbot with the FastAPI backend on Render and the Angular frontend on Vercel.

## Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
4. **Required API Keys**:
   - GROQ API Key or OpenAI API Key
   - MongoDB connection string (if using MongoDB)

## Part 1: Deploy Backend to Render

### Step 1: Prepare Environment Variables

1. Copy `backend/.env.example` to `backend/.env`
2. Fill in your actual values:
   ```env
   GROQ_API_KEY=your_actual_groq_key_here
   OPENAI_API_KEY=your_actual_openai_key_here
   MONGO_URI=your_actual_mongodb_connection_string
   CORS_ORIGINS=http://localhost:4200
   ```

### Step 2: Push to GitHub

```bash
# From your project root
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 3: Deploy on Render

1. **Login to Render**: Go to [render.com](https://render.com) and sign in
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `viztalk-ai-tutor-chatbot`

3. **Configure the Service**:
   - **Name**: `viztalk-ai-tutor-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free` (or paid plan for better performance)

4. **Set Environment Variables**:
   In the Render dashboard, go to Environment tab and add:
   ```
   GROQ_API_KEY=your_actual_groq_key
   OPENAI_API_KEY=your_actual_openai_key  
   MONGO_URI=your_mongodb_connection_string
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```
   **Note**: You'll update `CORS_ORIGINS` after deploying the frontend

5. **Deploy**: Click "Create Web Service"

6. **Get Backend URL**: After deployment, note your backend URL (e.g., `https://viztalk-ai-tutor-backend.onrender.com`)

## Part 2: Deploy Frontend to Vercel

### Step 1: Update Environment Configuration

1. Update `frontend/src/environments/environment.ts` with your Render backend URL:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-actual-render-backend-url.onrender.com'
   };
   ```

2. Commit and push changes:
   ```bash
   git add frontend/src/environments/environment.ts
   git commit -m "Update production API URL"
   git push origin main
   ```

### Step 2: Deploy on Vercel

1. **Login to Vercel**: Go to [vercel.com](https://vercel.com) and sign in
2. **Import Project**:
   - Click "New Project"
   - Import your GitHub repository
   - Select `viztalk-ai-tutor-chatbot`

3. **Configure the Project**:
   - **Framework Preset**: Angular
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (should auto-detect)
   - **Output Directory**: `dist/frontend/browser` (should auto-detect)
   - **Install Command**: `npm install` (should auto-detect)

4. **Deploy**: Click "Deploy"

5. **Get Frontend URL**: After deployment, note your frontend URL (e.g., `https://your-project-name.vercel.app`)

### Step 3: Update CORS Configuration

1. **Go back to Render dashboard**
2. **Update Environment Variables**:
   - Find your backend service
   - Go to Environment tab
   - Update `CORS_ORIGINS` to include your Vercel URL:
     ```
     CORS_ORIGINS=https://your-actual-vercel-url.vercel.app,http://localhost:4200
     ```
3. **Redeploy**: The service will automatically redeploy with new environment variables

## Part 3: Testing Your Deployment

### Test Backend
1. Visit your Render backend URL: `https://your-backend-url.onrender.com`
2. Check API docs: `https://your-backend-url.onrender.com/docs`
3. Test a simple endpoint to verify it's working

### Test Frontend
1. Visit your Vercel frontend URL: `https://your-frontend-url.vercel.app`
2. Test the chat functionality
3. Check browser console for any CORS or API connection errors

### Test Integration
1. Try sending a message through the frontend
2. Verify the frontend can successfully communicate with the backend
3. Check that all features work as expected

## Part 4: Custom Domains (Optional)

### For Render (Backend)
1. Go to your Render service dashboard
2. Click "Settings" → "Custom Domains"
3. Add your custom domain and follow DNS instructions

### For Vercel (Frontend)
1. Go to your Vercel project dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain and follow DNS instructions

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure `CORS_ORIGINS` in Render includes your exact Vercel URL
   - No trailing slashes in URLs
   - Include both `http://localhost:4200` and your production URL

2. **Build Failures**:
   - **Backend**: Check Dockerfile syntax, requirements.txt dependencies
   - **Frontend**: Ensure all dependencies in package.json, check Angular configuration

3. **Environment Variables**:
   - Verify all required environment variables are set in Render
   - Check that API keys are valid and have proper permissions

4. **API Connection Issues**:
   - Verify the frontend environment.ts has the correct backend URL
   - Ensure backend is responding (check /docs endpoint)
   - Check network tab in browser dev tools

### Logs and Debugging

1. **Render Logs**: Go to your service → "Logs" tab to see backend errors
2. **Vercel Logs**: Go to your project → "Functions" tab for build/runtime logs
3. **Browser Console**: Check for frontend errors and network issues

## Environment Variables Reference

### Backend (Render)
```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key  
MONGO_URI=your_mongodb_connection_string
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:4200
PORT=10000
```

### Frontend (Vercel)
No environment variables needed - configuration is handled through Angular environment files.

## Performance Tips

1. **Render**: 
   - Consider upgrading from free tier for better performance
   - Free tier sleeps after inactivity - first request may be slow

2. **Vercel**:
   - Optimize bundle size
   - Use lazy loading for routes
   - Consider upgrading for better analytics and performance

## Security Considerations

1. **API Keys**: Never commit real API keys to repository
2. **CORS**: Use specific origins instead of "*" in production
3. **HTTPS**: Both platforms provide HTTPS by default
4. **Rate Limiting**: Consider implementing rate limiting for production APIs

---

**Congratulations!** 🎉 Your AI Tutor Chatbot should now be live with:
- Backend: `https://your-backend.onrender.com`
- Frontend: `https://your-frontend.vercel.app`
