<script lang="ts">
  import { onMount } from 'svelte';
  import { invoke } from '@tauri-apps/api/core';
  import { fly } from 'svelte/transition';

  // --- Type Definitions for Backend Data ---
  interface JailbreakMethod {
    name: string;
    description: string;
  }

  interface JailbreakCategory {
    name: string;
    methods: JailbreakMethod[];
  }

  // --- State Management ---
  let aiModels = $state<string[]>([]);
  let jailbreakCategories = $state<JailbreakCategory[]>([]);
  let isLoading = $state(true);

  let selectedModel = $state('');
  let selectedMethod = $state(''); // This will now just be the method name string
  let customRestriction = $state('');
  let generatedPrompt = $state("");
  let errorMessage = $state('');
  let shouldShake = $state(false);

  // --- Fetch initial data from Rust backend ---
  onMount(async () => {
    isLoading = true;
    try {
      const modelsPromise = invoke<string[]>('get_ai_models');
      const categoriesPromise = invoke<JailbreakCategory[]>('get_jailbreak_methods');

      const [models, categories] = await Promise.all([modelsPromise, categoriesPromise]);

      aiModels = models;
      if (aiModels.length > 0) {
        selectedModel = aiModels[0];
      }

      jailbreakCategories = categories;
      // Set a default selection
      if (categories.length > 0 && categories[0].methods.length > 0) {
        selectedMethod = categories[0].methods[0].name;
      }
    } catch (e: any) {
      errorMessage = `Error fetching initial data: ${e.toString()}`;
      console.error(e);
    } finally {
      isLoading = false;
    }
  });

  // --- Core Functions (handleGenerate and handleCopy are unchanged) ---
  async function handleGenerate() {
    errorMessage = '';
    if (!customRestriction) {
      errorMessage = 'Please enter a custom restriction to bypass.';
      shouldShake = true;
      setTimeout(() => { shouldShake = false; }, 820); // Duration of the shake animation
      return;
    }
    try {
      const result: string = await invoke('generate_prompt', {
        model: selectedModel,
        method: selectedMethod,
        restriction: customRestriction,
      });
      generatedPrompt = result;
    } catch (e: any) {
      errorMessage = `Error generating prompt: ${e.toString()}`;
      console.error(e);
      generatedPrompt = `An error occurred: ${e.toString()}`;
    }
  }

  async function handleCopy() {
    if (!generatedPrompt) return;
    try {
      await navigator.clipboard.writeText(generatedPrompt);
    } catch (e: any) {
      errorMessage = `Error copying to clipboard: ${e.toString()}`;
      console.error(e);
    }
  }
</script>

<div class="app-container">
  <!-- Pane 1: AI Models -->
  <div class="pane pane-1" in:fly={{ x: -200, duration: 500, delay: 100 }}>
    <h2>AI Models</h2>
    {#if isLoading}
      <div>
        {#each Array(10) as _}
          <div class="skeleton skeleton-list-item"></div>
        {/each}
      </div>
    {:else}
      <select bind:value={selectedModel} size="10">
        {#each aiModels as model, i}
          <option value={model} transition:fly={{ y: 20, duration: 300, delay: i * 30 }}>
            {model}
          </option>
        {/each}
      </select>
    {/if}
  </div>

  <!-- Pane 2: Jailbreak Methods & Restriction -->
  <div class="pane pane-2" in:fly={{ y: -200, duration: 500, delay: 200 }}>
    <h2>Jailbreak Method</h2>
    {#if isLoading}
      <div class="skeleton skeleton-select"></div>
      <div class="skeleton skeleton-input"></div>
      <div class="skeleton skeleton-button"></div>
    {:else}
      <div class="method-list">
        {#each jailbreakCategories as category}
          <div class="category">
            <h3 class="category-title">{category.name}</h3>
            <ul class="method-items">
              {#each category.methods as method, i}
                <li
                  class="method-item"
                  class:selected="{selectedMethod === method.name}"
                  on:click={() => selectedMethod = method.name}
                  transition:fly={{ y: 20, duration: 300, delay: i * 30 }}
                >
                  <strong>{method.name}</strong>
                  <p>{method.description}</p>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>

      <div style="margin-top: auto;"> <!-- Pushes following elements to the bottom -->
        <label for="custom-restriction">Custom Restriction to Bypass</label>
        <input
          type="text"
          id="custom-restriction"
          placeholder="e.g., 'refusal to generate harmful code'"
          bind:value={customRestriction}
          class:error-shake={shouldShake}
        />
        <button type="button" on:click={handleGenerate} style="width: 100%; margin-top: 10px;">
          Generate Prompt
        </button>
      </div>
    {/if}
    {#if errorMessage}
      <p style="color: #ff4d4d; font-size: 0.9rem; margin-top: 10px;">{errorMessage}</p>
    {/if}
  </div>

  <!-- Pane 3: Output -->
  <div class="pane pane-3" in:fly={{ x: 200, duration: 500, delay: 300 }}>
    <div class="output-container">
      <div class="output-header">
        <h2>Generated Prompt</h2>
        <button type="button" class="copy-button" on:click={handleCopy}>Copy</button>
      </div>
      <textarea readonly placeholder="Generated prompt will appear here..." bind:value={generatedPrompt}></textarea>
    </div>
  </div>
</div>
