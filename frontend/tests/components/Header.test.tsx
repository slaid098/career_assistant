import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from '@/components/Header';
import '@testing-library/jest-dom';

describe('Header Component', () => {
  it('should render the header with the site title', () => {
    render(<Header />);
    const titleElement = screen.getByText('Career Assistant');
    expect(titleElement).toBeInTheDocument();
  });

  it('should have a link to the homepage', () => {
    render(<Header />);
    const linkElement = screen.getByRole('link', { name: 'Career Assistant' });
    expect(linkElement).toHaveAttribute('href', '/');
  });

  it('should match the snapshot', () => {
    const { container } = render(<Header />);
    expect(container).toMatchSnapshot();
  });
}); 