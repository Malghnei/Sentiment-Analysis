<script lang="ts">
  import Papa from 'papaparse';

  let { onParsed } = $props<{ onParsed: (data: string[]) => void }>();
  let isDragging = $state(false);
  let fileInput: HTMLInputElement;

  async function processFile(file: File) {
    console.log('CsvUploader: processing file:', file.name, file.size, file.type);
    if (!file.name.toLowerCase().endsWith('.csv')) {
      alert('Please upload a valid CSV file.');
      return;
    }

    try {
      console.log('CsvUploader: reading file text...');
      const csvText = await file.text();
      console.log('CsvUploader: file text read, length:', csvText.length);
      
      console.log('CsvUploader: parsing CSV with PapaParse...');
      const results = Papa.parse<any>(csvText, {
        header: true,
        skipEmptyLines: true
      });

      console.log('CsvUploader: parse results:', {
        dataCount: results.data?.length,
        errors: results.errors,
        meta: results.meta
      });

      if (results.data && results.data.length > 0) {
        // Try to find the text column
        const headers = results.meta.fields || Object.keys(results.data[0]);
        console.log('CsvUploader: detected headers:', headers);
        
        const firstRow = results.data[0] as any;
        const textKey = Object.keys(firstRow).find(key => 
          key.toLowerCase().includes('text') || key.toLowerCase().includes('review') || key.toLowerCase().includes('message') || key.toLowerCase().includes('content')
        ) || Object.keys(firstRow)[0];

        if (textKey) {
          console.log('CsvUploader: using column for text:', textKey);
          const parsedData = results.data
            .map((row: any) => row[textKey])
            .filter((val: any) => val && val.toString().trim() !== '');

          console.log('CsvUploader: calling onParsed with', parsedData.length, 'items');
          onParsed(parsedData);
        } else {
          console.error('CsvUploader: No text columns found');
          alert('Could not find a text column in the CSV. Please ensure your CSV has a "text" header.');
        }
      } else {
        console.warn('CsvUploader: CSV is empty or parsing failed');
        alert('The CSV file appears to be empty or could not be parsed.');
      }
    } catch (error: any) {
      console.error('CsvUploader: Exception in processFile:', error);
      alert('Error reading CSV file: ' + error.message);
    }
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
    console.log('CsvUploader: file dropped');
    if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
    }
  }

  function handleFileSelect(e: Event) {
    const target = e.target as HTMLInputElement;
    console.log('CsvUploader: file selected via input');
    if (target.files && target.files.length > 0) {
      processFile(target.files[0]);
    }
    // reset input so the same file could be selected again
    target.value = '';
  }

  function handleDragEnter(e: DragEvent) {
    e.preventDefault();
    isDragging = true;
    console.log('CsvUploader: drag enter');
  }

  function handleDragLeave(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
    console.log('CsvUploader: drag leave');
  }
</script>

<label 
  class="relative border-2 border-dashed rounded-xl p-12 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer group bg-neutral-200/50 hover:bg-neutral-400/50 hover:border-indigo-500/50 w-full {isDragging ? 'border-indigo-500 bg-indigo-500/10' : ''}"
  ondragenter={handleDragEnter}
  ondragover={(e) => e.preventDefault()}
  ondragleave={handleDragLeave}
  ondrop={handleDrop}
>
  <input 
    type="file" 
    accept=".csv" 
    class="hidden" 
    bind:this={fileInput}
    onchange={handleFileSelect} 
  />
  
  <div class="mb-4 p-4 rounded-full bg-indigo-500/10 text-indigo-400 group-hover:scale-110 transition-transform duration-300">
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
  </div>
  
  <h3 class="text-lg font-medium text-black mb-2">Upload CSV File</h3>
  <p class="text-neutral-400 text-center text-sm mb-4">
    Drag and drop your file here or <span class="text-indigo-400 font-semibold group-hover:underline">browse local files</span>
  </p>
  
  <div class="flex gap-4 text-xs text-neutral-500">
    <div class="flex items-center gap-1">
      <div class="w-1 h-1 rounded-full bg-indigo-500"></div>
      <span>Header: text</span>
    </div>
    <div class="flex items-center gap-1">
      <div class="w-1 h-1 rounded-full bg-indigo-500"></div>
      <span>Format: .csv</span>
    </div>
  </div>
</label>

