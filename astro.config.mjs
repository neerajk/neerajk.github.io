// @ts-check
import { defineConfig } from 'astro/config';

// User site: the repo must be named neerajk.github.io, so no `base` is needed.
// For a project repo (e.g. github.com/neerajk/portfolio) add: base: '/portfolio'
export default defineConfig({
  site: 'https://neerajk.github.io',
});
