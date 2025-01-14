export type RouteParams = {
  id: string;
};

export type Member = {
  displayname: string;
  email: string;
  id: string;
  roles: string[];
  username: string;
  current_user: boolean;
};

export type BrandStores = {
  brandStores: {
    brandStoresList: Array<{}>;
  };
};

export type CurrentStore = {
  currentStore: {
    currentStore: {
      id: string;
      "manual-review-policy": string;
      private: boolean;
    };
  };
};

export type Snaps = {
  snaps: {
    snaps: Array<{}>;
  };
};

export type Invites = {
  invites: {
    invites: Array<{}>;
  };
};

export type Members = {
  members: {
    members: Array<Member>;
  };
};
