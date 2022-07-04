import Typography, { TypographyProps } from '@mui/material/Typography';

export type TitleProps = Omit<TypographyProps<'h1'>, 'component' | 'variant'>;
export type SubTitleProps = Omit<TypographyProps<'h2'>, 'component' | 'variant'>;
export type ParagraphProps = Omit<TypographyProps<'p'>, 'component'>;

export const Title = (props: TitleProps) => <Typography component="h1" variant="h4" {...props} />;

export const SubTitle = (props: SubTitleProps) => (
  <Typography component="h2" variant="h5" {...props} />
);

export const Paragraph = (props: ParagraphProps) => <Typography component="p" {...props} />;
