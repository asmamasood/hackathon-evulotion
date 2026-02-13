# Component Architecture Skill

## Purpose
Structure reusable and maintainable React components with proper separation of concerns.

## Implementation Guidelines
- Create atomic design system (atoms, molecules, organisms)
- Separate presentational and container components
- Implement proper prop drilling or state management
- Use TypeScript for type safety
- Follow consistent naming conventions

## Best Practices
- Keep components focused on single responsibilities
- Use composition over inheritance
- Implement proper error boundaries
- Optimize components with React.memo when appropriate
- Follow accessibility best practices

## Example Usage
```
// Atoms
<Button variant="primary" onClick={handleClick}>
  Submit
</Button>

// Molecules
<InputField
  label="Email"
  type="email"
  value={email}
  onChange={setEmail}
/>

// Organisms
<UserProfileForm onSubmit={handleSubmit} />

// Templates
<MainLayout>
  <UserProfileForm />
</MainLayout>
```