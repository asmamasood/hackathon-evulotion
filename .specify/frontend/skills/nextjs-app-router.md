# Next.js App Router Skill

## Purpose
Implement Next.js App Router structure with proper component organization and routing.

## Implementation Guidelines
- Use the app directory structure for routing
- Implement Server and Client components appropriately
- Follow Next.js conventions for file-based routing
- Use React Server Components by default for better performance
- Leverage React Server Functions for data fetching

## Best Practices
- Organize components in the app directory using folders
- Use loading.js and error.js for better UX
- Implement proper metadata for SEO
- Use dynamic imports for code splitting
- Follow Next.js image optimization practices

## Example Usage
```
// app/page.tsx
import { getData } from '@/lib/data-fetch'

export default async function HomePage() {
  const data = await getData()
  
  return (
    <div>
      <h1>Home Page</h1>
      <Component data={data} />
    </div>
  )
}

// app/products/[id]/page.tsx
export default async function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h1>Product {params.id}</h1>
    </div>
  )
}
```