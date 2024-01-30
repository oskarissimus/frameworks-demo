<template>
  <button @click="count++">Click me</button>
  <p>You clicked {{ count }} times.</p>
</template>

<script>
export default {
  data() {
    return {
      count: 0
    };
  }
}
</script>
