prompts: any[] = [];

ngOnInit() {
  this.service.getPrompts().subscribe((res: any) => {
    this.prompts = res;
  });
}
