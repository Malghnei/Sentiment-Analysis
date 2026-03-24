<script lang="ts">
  import { env } from '$env/dynamic/public';
  import CsvUploader from '$lib/components/CsvUploader.svelte';

  // State
  let inputText = $state('');
  let isLoading = $state(false);
  let results = $state<Array<{text: string, vader: any, roberta: any}>>([]);
  let errorMsg = $state('');
  
  // API URL from .env, fallback to localhost for tests
  const API_URL = env.PUBLIC_AWS_API_URL || 'http://localhost:3000';

  async function analyzeText(texts: string[]) {
    if (!texts.length) return;
    
    isLoading = true;
    errorMsg = '';
    
    // Quick validation limit to prevent freezing browser on huge batches
    const limitTexts = texts.slice(0, 100);
    console.log('analyzeText: sending request to:', `${API_URL}/analyze`);
    console.log('analyzeText: texts count:', limitTexts.length);
    
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texts: limitTexts })
      });
      
      console.log('analyzeText: response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('analyzeText: server error:', errorText);
        throw new Error(`API error: ${response.status} - Could not connect to backend`);
      }
      
      const data = await response.json();
      console.log('analyzeText: received data:', data);
      // Prepend to results, keeping the latest at the top
      results = [...data.results, ...results];
    } catch (err: any) {
      console.error('analyzeText: fetch error:', err);
      errorMsg = err.message || 'An error occurred during analysis';
    } finally {
      isLoading = false;
      inputText = '';
    }
  }


  function handleSingleSubmit() {
    if (inputText.trim()) {
      analyzeText([inputText.trim()]);
    }
  }

  // Use the HTML event form instead of the custom on:click to conform to Svelte 5 best practices,
  // but standard on:click also works fine in most contexts.
</script>

<svelte:head>
  <title>Sentiment Analysis Playground</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
  <div class="max-w-4xl mx-auto space-y-8">
    <div class="text-center">
      <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">Sentiment Analysis</h1>
      <p class="mt-3 max-w-2xl mx-auto text-lg text-gray-500 sm:mt-4">
        Discover contextual nuances by comparing <span class="text-blue-600 font-semibold text-sm bg-blue-50 px-2 py-0.5 rounded">VADER</span> and <span class="text-purple-600 font-semibold text-sm bg-purple-50 px-2 py-0.5 rounded">RoBERTa</span> analysis.
      </p>
    </div>

    <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-6">
      <div>
        <label for="text-input" class="block text-sm font-medium text-gray-700">Test it out on a single snippet</label>
        <div class="mt-2">
          <textarea
            id="text-input"
            rows="3"
            class="shadow-sm p-4 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border border-gray-200 rounded-xl"
            placeholder="e.g. The flight was delayed, but the crew was incredibly nice!"
            bind:value={inputText}
          ></textarea>
        </div>
        <div class="mt-3">
          <button
            onclick={handleSingleSubmit}
            disabled={isLoading || !inputText.trim()}
            class="inline-flex items-center px-5 py-2.5 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {#if isLoading}
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            {:else}
              Analyze Text
            {/if}
          </button>
        </div>
      </div>

      <div class="relative py-2">
        <div class="absolute inset-0 flex items-center" aria-hidden="true">
          <div class="w-full border-t border-gray-200"></div>
        </div>
        <div class="relative flex justify-center">
          <span class="px-3 bg-white text-xs font-semibold tracking-widest text-gray-400 uppercase">Or Batch Process</span>
        </div>
      </div>

      <div>
        <CsvUploader onParsed={(data: string[]) => analyzeText(data)} />
      </div>
    </div>

    {#if errorMsg}
      <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-md">
        <div class="flex">
          <div class="ml-3 text-sm text-red-700">
            <p class="font-bold">Execution Failed</p>
            <p>{errorMsg}</p>
          </div>
        </div>
      </div>
    {/if}

    {#if results.length > 0}
      <div class="bg-white shadow-sm border border-gray-100 rounded-2xl overflow-hidden mt-8">
        <div class="px-6 py-5 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
          <h3 class="text-base font-semibold text-gray-900">Analysis Results</h3>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
            {results.length} items
          </span>
        </div>
        <ul class="divide-y divide-gray-100 text-sm">
          {#each results as result}
            <li class="px-6 py-6 hover:bg-gray-50/50 transition-colors">
              <div class="mb-4 text-gray-800 text-base leading-relaxed">"{result.text}"</div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                <!-- VADER Result -->
                <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                      <span class="w-2 h-2 rounded-full {result.vader.score > 0.05 ? 'bg-green-500' : result.vader.score < -0.05 ? 'bg-red-500' : 'bg-gray-400'}"></span>
                      <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">VADER</span>
                    </div>
                    <span class="font-semibold px-2 py-0.5 rounded text-xs
                      {result.vader.label === 'POSITIVE' ? 'bg-green-100 text-green-800' : 
                       result.vader.label === 'NEGATIVE' ? 'bg-red-100 text-red-800' : 
                       'bg-gray-100 text-gray-800'}">
                      {result.vader.label}
                    </span>
                  </div>
                  <!-- Progress Bar equivalent -->
                  <div class="relative w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <!-- Base marker at 0 -->
                    <div class="absolute w-px h-full bg-gray-400 left-1/2 z-10"></div>
                    <!-- Fill -->
                    <div class="absolute h-full rounded-full transition-all duration-500 {result.vader.score >= 0 ? 'bg-green-500 left-1/2' : 'bg-red-500 right-1/2'}" 
                         style="width: {Math.abs(result.vader.score) * 50}%"></div>
                  </div>
                  <div class="text-right mt-1.5 text-xs text-gray-400 font-mono">{(result.vader.score).toFixed(3)}</div>
                </div>
                
                <!-- RoBERTa Result -->
                <div class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                      <span class="w-2 h-2 rounded-full {result.roberta.score > 0.1 ? 'bg-purple-500' : result.roberta.score < -0.1 ? 'bg-red-500' : 'bg-gray-400'}"></span>
                      <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">RoBERTa</span>
                    </div>
                    <span class="font-semibold px-2 py-0.5 rounded text-xs
                      {result.roberta.label === 'POSITIVE' ? 'bg-purple-100 text-purple-800' : 
                       result.roberta.label === 'NEGATIVE' ? 'bg-red-100 text-red-800' : 
                       'bg-gray-100 text-gray-800'}">
                      {result.roberta.label}
                    </span>
                  </div>
                  <!-- Progress Bar equivalent -->
                  <div class="relative w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <!-- Base marker at 0 -->
                    <div class="absolute w-px h-full bg-gray-400 left-1/2 z-10"></div>
                    <!-- Fill -->
                    <div class="absolute h-full rounded-full transition-all duration-500 {result.roberta.score >= 0 ? 'bg-purple-500 left-1/2' : 'bg-red-500 right-1/2'}" 
                         style="width: {Math.abs(result.roberta.score) * 50}%"></div>
                  </div>
                  <div class="text-right mt-1.5 text-xs text-gray-400 font-mono">{(result.roberta.score).toFixed(3)}</div>
                </div>
                
              </div>
            </li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
</div>
