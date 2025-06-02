<script>
  import { onMount } from 'svelte';
  let source = '';
  let destination = '';
  let distance = null;
  let history = [];

  const getDistance = async () => {
    const res = await fetch('http://localhost:8000/distance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source, destination })
    });
    const data = await res.json();
    distance = data.distance_km;
    fetchHistory();
  };

  const fetchHistory = async () => {
    const res = await fetch('http://localhost:8000/history');
    history = await res.json();
  };

  onMount(() => {
    fetchHistory();
  });
</script>

<h1>Distance Calculator</h1>
<input bind:value={source} placeholder="Source Address" />
<input bind:value={destination} placeholder="Destination Address" />
<button on:click={getDistance}>Calculate Distance</button>

{#if distance !== null}
  <p>Distance: {distance.toFixed(2)} km</p>
{/if}

<h2>History</h2>
<ul>
  {#each history as item}
    <li>{item.source} to {item.destination}: {item.distance_km.toFixed(2)} km at {new Date(item.timestamp).toLocaleString()}</li>
  {/each}
</ul>
